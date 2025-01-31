from rest_framework import generics,status
from rest_framework.response import Response
from .serializers import (RegistrationSerializer,CustomAuthTokenSerializer,
                          ChangePasswordSerializer,ProfileSerializer)
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import get_user_model
from ...models import Profile
from django.shortcuts import get_object_or_404
# from django.core.mail import send_mail
from mail_templated import send_mail,EmailMessage
from .utils import EmailThreading
from rest_framework_simplejwt.tokens import RefreshToken


User=get_user_model()

class RegistrationApiView(generics.GenericAPIView):
    serializer_class=RegistrationSerializer

    def post(self,request,*args,**kwargs):
        serializer=RegistrationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            data={
                'email':serializer.validated_data['email']
            }
            return Response(data,status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)


class CustomAuthToken(ObtainAuthToken):
    serializer_class=CustomAuthTokenSerializer
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'user_id': user.pk,
            'email': user.email
        })
    
    
class CustomDiscardAuthToken(APIView):
    permission_classes=[IsAuthenticated]

    def post (self,request):
        request.user.auth_token.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
'''Define view for change password'''
class ChangePasswordApiView(generics.UpdateAPIView):
    model=User
    permission_classes=[IsAuthenticated]
    serializer_class=ChangePasswordSerializer

    def get_object(self,queryset=None):
        obj=self.request.user
        return obj
    
    def put(self, request, *args, **kwargs):
        self.object=self.get_object()
        serializer=self.get_serializer(data=request.data)
        if serializer.is_valid():
            #check old password
            if not self.object.check_password(serializer.data.get('old_password')):
                return Response({'old_password':['wrong password.']}, status=status.HTTP_400_BAD_REQUEST)
            # set_password also hashes that
            self.object.set_password(serializer.data.get("new_password"))
            self.object.save()
            return Response({'details':'password changed successfully'},status=status.HTTP_200_OK)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    
'''Define view for show or edit Profile'''
class ProfileApiView(generics.RetrieveUpdateAPIView):
    serializer_class=ProfileSerializer
    queryset=Profile.objects.all()

    def get_object(self):
        queryset=self.get_queryset()
        obj=get_object_or_404(queryset,user=self.request.user)
        return obj
    
'''Define view for send mail for verification'''
class TestEmailSend(generics.GenericAPIView):

    def get(self,request,*args,**kwargs):
        '''send_mail(
            'Verification email',
            'Your verify code is: ...',
            'from@example.com',
            ['to@example.com'],
            fail_silently=False,
        )'''
        # send_mail('email/verify.tpl',{'name': 'fazel'}, 'from@example.com',['to@example.com'])
        self.email='fazelkalhory@gmail.com'
        user_obj=get_object_or_404(User,email=self.email)
        token=self.get_token_for_user(user_obj)
        email_obj=EmailMessage('email/verify.tpl',{'token': token}, 'from@example.com',to=[self.email])
        EmailThreading(email_obj).start()
        return Response ("Email sent")
    
    def get_token_for_user(self,user):
        refresh=RefreshToken.for_user(user)
        return str(refresh.access_token)