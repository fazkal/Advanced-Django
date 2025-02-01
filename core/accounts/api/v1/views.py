from rest_framework import generics, status
from rest_framework.response import Response
from .serializers import (
    RegistrationSerializer,
    CustomAuthTokenSerializer,
    ActivationResendSerializer,
    ChangePasswordSerializer,
    ProfileSerializer,
)
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import get_user_model
from ...models import Profile
from django.shortcuts import get_object_or_404

# from django.core.mail import send_mail
from mail_templated import send_mail, EmailMessage
from .utils import EmailThreading
from rest_framework_simplejwt.tokens import RefreshToken
import jwt
from jwt.exceptions import ExpiredSignatureError, InvalidSignatureError
from django.conf import settings

User = get_user_model()


# Define view for registration account
class RegistrationApiView(generics.GenericAPIView):
    serializer_class = RegistrationSerializer

    def post(self, request, *args, **kwargs):
        serializer = RegistrationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            email = serializer.validated_data["email"]
            data = {"email": email}
            user_obj = get_object_or_404(User, email=email)
            token = self.get_token_for_user(user_obj)
            email_obj = EmailMessage(
                "email/verify.tpl", {"token": token}, "from@example.com", to=[email]
            )
            EmailThreading(email_obj).start()
            return Response(data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get_token_for_user(self, user):
        refresh = RefreshToken.for_user(user)
        return str(refresh.access_token)


# Define view for verify account
class ActivationApiView(APIView):

    def get(self, request, token, *args, **kwargs):
        try:
            token = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
            user_id = token.get("user_id")
        except ExpiredSignatureError:
            return Response(
                {"Details": "Token has been expired"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        except InvalidSignatureError:
            return Response(
                {"Details": "Token is not valid"}, status=status.HTTP_400_BAD_REQUEST
            )
        user_obj = User.objects.get(pk=user_id)

        if user_obj.is_verified:
            return Response({"Details": "Your account has already been verified"})
        user_obj.is_verified = True
        user_obj.save()
        return Response(
            {"Details": "Your account have been verified and activated successfully"}
        )


# Define view for resend email of token activation account
class ActivationResendApiView(generics.GenericAPIView):
    serializer_class = ActivationResendSerializer

    def post(self, request, *args, **kwargs):
        serializer = ActivationResendSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user_obj = serializer.validated_data["user"]
        token = self.get_token_for_user(user_obj)
        email_obj = EmailMessage(
            "email/verify.tpl",
            {"token": token},
            "from@example.com",
            to=[user_obj.email],
        )
        EmailThreading(email_obj).start()
        return Response(
            {"Details": "User activation resend successfully"},
            status=status.HTTP_200_OK,
        )

    def get_token_for_user(self, user):
        refresh = RefreshToken.for_user(user)
        return str(refresh.access_token)


# Define view for generate token of account
class CustomAuthToken(ObtainAuthToken):
    serializer_class = CustomAuthTokenSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(
            data=request.data, context={"request": request}
        )
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data["user"]
        token, created = Token.objects.get_or_create(user=user)
        return Response({"token": token.key, "user_id": user.pk, "email": user.email})


# Define view for discard token of account
class CustomDiscardAuthToken(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        request.user.auth_token.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# Define view for change password
class ChangePasswordApiView(generics.UpdateAPIView):
    model = User
    permission_classes = [IsAuthenticated]
    serializer_class = ChangePasswordSerializer

    def get_object(self, queryset=None):
        obj = self.request.user
        return obj

    def put(self, request, *args, **kwargs):
        self.object = self.get_object()
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            # check old password
            if not self.object.check_password(serializer.data.get("old_password")):
                return Response(
                    {"old_password": ["wrong password."]},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            # set_password also hashes that
            self.object.set_password(serializer.data.get("new_password"))
            self.object.save()
            return Response(
                {"details": "password changed successfully"}, status=status.HTTP_200_OK
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Define view for show or edit Profile
class ProfileApiView(generics.RetrieveUpdateAPIView):
    serializer_class = ProfileSerializer
    queryset = Profile.objects.all()

    def get_object(self):
        queryset = self.get_queryset()
        obj = get_object_or_404(queryset, user=self.request.user)
        return obj


# Define view for send mail for test mail
class TestEmailSend(generics.GenericAPIView):

    def get(self, request, *args, **kwargs):
        """send_mail(
            'Verification email',
            'Your verify code is: ...',
            'from@example.com',
            ['to@example.com'],
            fail_silently=False,
        )"""
        # send_mail('email/verify.tpl',{'name': 'fazel'}, 'from@example.com',['to@example.com'])
        self.email = "fazelkalhory@gmail.com"
        user_obj = get_object_or_404(User, email=self.email)
        token = self.get_token_for_user(user_obj)
        email_obj = EmailMessage(
            "email/verify.tpl", {"token": token}, "from@example.com", to=[self.email]
        )
        EmailThreading(email_obj).start()
        return Response("Email sent")

    def get_token_for_user(self, user):
        refresh = RefreshToken.for_user(user)
        return str(refresh.access_token)
