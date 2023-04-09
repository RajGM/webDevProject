from rest_framework import serializers
from .models import *

#User serializer  model
class AppUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = AppUser
        fields = ['profileImage', 'dateOfBirth', 'bio']

#Post serializer model
class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ['postId', 'user', 'postDate', 'text', 'media', 'likes']

#User and post serializer model
class UserSerializer(serializers.ModelSerializer):
    profile = AppUserSerializer(read_only=True)
    posts = PostSerializer(many=True, read_only=True)
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name','profile','posts']

#Follower serializer model
class FollowerSerializer(serializers.ModelSerializer):
    class Meta:
        model=Follower
        fields=['user', 'follower', 'chat_room']
