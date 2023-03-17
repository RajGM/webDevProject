from django.shortcuts import render
from .models import *
from .forms import *
from .serializers import *
#from django.http import HttpResponseRedirect, HttpResponse
#from django.views.generic import ListView, DetailView, CreateView, DeleteView, UpdateView
#from django.contrib.auth import authenticate, login, logout
#from django.contrib.auth.decorators import login_required
#import os
#from datetime import datetime
#from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.renderers import TemplateHTMLRenderer
#from rest_framework import status, generics, mixins
from rest_framework.views import APIView

class PostView(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'home_base.html'

    def get(self, request):
        user = request.user
        queryset = Post.objects.all().order_by('-postId')
        if user.is_authenticated:
            user_profile = AppUser.objects.get(user=user)
            following_list=[]
            followings = Follower.objects.filter(follower=request.user)
            for following in followings:
                following_list.append(following)
            if user_profile.profileImage:
                image_url = user_profile.profileImage.url
            else:
                image_url = None

            return Response({'posts':queryset, 'user_profile':user_profile, 'img_url':image_url, 'user':user,'following_list':following_list})

        return Response({'posts':queryset, 'user_profile':None, 'img_url':None, 'user':user,'following_list':None})