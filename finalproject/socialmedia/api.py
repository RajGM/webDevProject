from .models import *
from .serializers import *
from rest_framework import generics, mixins

#API for username
class UserList(generics.ListAPIView):
    serializer_class = UserSerializer

    def get_queryset(self):
        username = self.kwargs['username']
        user = User.objects.filter(username=username)
        return user

#API for postId
class PostByID(generics.ListAPIView):
    serializer_class = PostSerializer

    def get_queryset(self):
        postId = self.kwargs['pk']
        return Post.objects.filter(postId=postId)

#API for post list
class PostList(generics.ListAPIView, mixins.CreateModelMixin):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)
