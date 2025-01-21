from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from .serializers import PostSerializer,CategorySerializer
from ...models import Post,Category
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework import mixins,viewsets
from rest_framework.generics import GenericAPIView,ListAPIView,ListCreateAPIView,RetrieveUpdateDestroyAPIView

""" function base api views: 
"Getting a list of posts and creating new posts:"
from rest_framework.decorators import api_view,permission_classes
@api_view(["GET","POST"])
@permission_classes([IsAuthenticatedOrReadOnly])
def postList(request):
    if request.method=="GET":
        posts=Post.objects.filter(status=True)
        serializer=PostSerializer(posts,many=True)
        return Response(serializer.data)
    elif request.method=="POST":
        serializer=PostSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

@api_view(["GET","PUT","DELETE"])
@permission_classes([IsAuthenticatedOrReadOnly])
def postDetail(request,id):
    post=get_object_or_404(Post,pk=id,status=True)
    if request.method=="GET":
        serializer=PostSerializer(post)
        return Response(serializer.data)
    elif request.method=="PUT":
        serializer=PostSerializer(post,data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
    elif request.method=="DELETE":
        post.delete()
        return Response({"Detail":"Item removed successfully"})"""

""" Class base api views: """
#inherited from ModelViewSet
class PostModelViewSet(viewsets.ModelViewSet):
    permission_classes=[IsAuthenticatedOrReadOnly]
    serializer_class=PostSerializer
    queryset=Post.objects.filter(status=True)

class CategoryModelViewSet(viewsets.ModelViewSet):
    permission_classes=[IsAuthenticatedOrReadOnly]
    serializer_class=CategorySerializer
    queryset=Category.objects.all()

'''inherited from GenericAPIView
class PostList(ListCreateAPIView):
    """Getting a list of posts and creating new posts"""
    permission_classes=[IsAuthenticatedOrReadOnly]
    serializer_class=PostSerializer
    #When inherited from ListCreateAPIView and GenericAPIView with ListModel and CreateModel mixins:
    queryset=Post.objects.filter(status=True)'''


'''inherited from GenericAPIView with ListModel and CreateModel mixins
    def get(self,request,*args,**kwargs):
        """Retrieving a list of posts """
        return self.list(request,*args,**kwargs)
    
    def post(self,request,*args,**kwargs):
        return self.create(request,*args,**kwargs)'''

'''Inherited from APIView
    def get(self,request):
        """Retrieving a list of posts """
        posts=Post.objects.filter(status=True)
        serializer=PostSerializer(posts,many=True)
        return Response(serializer.data)
    
    def post(self,request):
        """Creating a post with providing data"""
        serializer=PostSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)'''
    
class PostDetail(RetrieveUpdateDestroyAPIView):
    """Getting detail of the post and and edit plus removing it"""
    permission_classes=[IsAuthenticatedOrReadOnly]
    serializer_class=PostSerializer
    #When inherited from RetrieveUpdateDestroyAPIView:
    queryset=Post.objects.filter(status=True)

'''Inherited from APIView
    def get(self,request,id):
        """Retrieving the post data """
        post=get_object_or_404(Post,pk=id,status=True)
        serializer=self.serializer_class(post)
        return Response(serializer.data)
    
    def put(self,request,id):
        """Editing the post data"""
        post=get_object_or_404(Post,pk=id,status=True)
        serializer=self.serializer_class(post,data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
    
    def delete(self,request,id):
        """Deleting the post object"""
        post=get_object_or_404(Post,pk=id,status=True)
        post.delete()
        return Response({"Detail":"Item removed successfully"})'''