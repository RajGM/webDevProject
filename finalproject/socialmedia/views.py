from django.shortcuts import render
from .models import *
from .forms import *
from .serializers import *
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from datetime import datetime
from rest_framework.response import Response
from rest_framework.renderers import TemplateHTMLRenderer
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
    

#Search users
def user_search(request):
    if request.method == "POST":
        search = request.POST['q']
        if search:
            result=User.objects.filter(username__contains=search)
            images = []
            for user in result:
                profile_result=AppUser.objects.get(user=user)
                if profile_result.profileImage:
                    profile_img = profile_result.profileImage.url
                    images.append(profile_img)
                else:
                    images.append(None)
            search_result = zip(result, images)
            return render(request, "search_user.html",{'search_result':search_result})
        else:
            return render(request, 'search_user.html')
    else:
        return HttpResponseRedirect("/")
    
#Register user
def register(request):
    registered = False

    if request.method == 'POST':
        user_form = UserForm(data=request.POST)
        profile_form = UserProfileForm(request.POST, request.FILES)
        if user_form.is_valid() and profile_form.is_valid(): #form validation
            user = user_form.save()
            user.set_password(user.password)
            user.save()
            profile = profile_form.save(commit=False)
            profile.user = user
            profile.save()
            registered=True
    else:
        user_form = UserForm()
        profile_form = UserProfileForm()

    return render(request, 'signup.html', {'user_form': user_form, 'profile_form':profile_form, 'registered':registered})

#User login
def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect('/')
            else:
                return HttpResponse("Your account is disable")
        else:
            return HttpResponse("Invalid login")
    return render(request, 'login.html', {})

#User logout
def user_logout(request):
    logout(request)
    return render(request, "logout.html")

#User fetch and update
@login_required
def user_profile(request):
    user = request.user
    if user.is_authenticated:
        user_profile = AppUser.objects.get(user=user)
        if user_profile.profileImage:
            image_url = user_profile.profileImage.url
            old_image_url = user_profile.profileImage.path
        else:
            image_url= None
            old_image_url = None

        if request.method == "POST":
            user_form = UserFormUpdate(request.POST or None, instance=user)
            user_profile_form = UserProfileFormUpdate(request.POST or None, request.FILES, instance=user_profile, initial={})
            if user_form.is_valid() and user_profile_form.is_valid():#form validation
                user_form.save()
                if user_profile.profileImage:
                    new_image_url = user_profile.profileImage.path
                    if old_image_url==new_image_url:
                        user_profile_form.save()
                    elif old_image_url==None:
                        user_profile_form.save()
                    else:
                        os.remove(old_image_url)
                        user_profile_form.save()
                else:
                    user_profile_form.save()
                return HttpResponseRedirect('/profile')
        else:
            user_form = UserFormUpdate(instance=user)
            user_profile_form = UserProfileFormUpdate(instance=user_profile)
    else:
        return HttpResponseRedirect('/login')

    return render(request, "user_profile.html", {"user":user, "user_profile":user_profile, "img_url":image_url, "user_form":user_form, "profile_form":user_profile_form})


#LoggedIn homepage
@login_required
def main_user_home(request):
    user = request.user
    if user.is_authenticated:
        user_profile = AppUser.objects.get(user=user)
        if user_profile.profileImage:
            img_url = user_profile.profileImage.url
        else:
            img_url = None
        if request.method=="POST":
            post_form = NewPostForm(request.POST, request.FILES)
            if post_form.is_valid(): #form validation
                post_form.save(user=user, time=datetime.now())
        else:
            post_form = NewPostForm()

        
        post = Post.objects.filter(user=user).order_by('-postId')
        follower_count = Follower.objects.filter(user=request.user).count()
        following_count = Follower.objects.filter(follower=request.user).count()

    else:
        return HttpResponseRedirect('/login')
    
    return render(request, "user_home.html", {"user_profile":user_profile, "img_url":img_url, "post_form":post_form, "posts":post, "follower_count":follower_count, "following_count":following_count})

#list of follower and following
def network_list(request):
    if request.method == "GET":
        follower_list=[]
        followers = Follower.objects.filter(user=request.user)
        for user in followers:
            follower_list.append(user)

        following_list=[]
        followings = Follower.objects.filter(follower=request.user)
        for user in followings:
            following_list.append(user)
        return render(request, "network.html", {"follower_list":follower_list, "following_list":following_list})
    else:
        return HttpResponseRedirect("user_home/")

#Common Home View 
class UserHome(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = "user.html"

    def get(self, request, username):#get user's information
        if Follower.objects.filter(user=username, follower=request.user):
            following=True
        else:
            following=False

        queryset = User.objects.get(username=username)
        user = UserSerializer(queryset)
        if queryset.profile.profileImage:
            img_url = user.data['profile']['profileImage']
        else:
            img_url = None

        follower_count = Follower.objects.filter(user=username).count()
        following_count = Follower.objects.filter(follower=username).count()

        return Response({"subuser":queryset, "user_profile": user.data['profile'], "img_url": img_url, "posts":user.data['posts'], "following":following, "follower_count":follower_count, "following_count":following_count})

    def post(self, request, username):
        queryset = User.objects.get(username=username)
        user = UserSerializer(queryset)
        if queryset.profile.profileImage:
            img_url = user.data['profile']['profileImage']
        else:
            img_url = None

        follower_count = Follower.objects.filter(user=username).count()
        following_count = Follower.objects.filter(follower=username).count()

        if request.method=="POST": 
            if Follower.objects.filter(user=username, follower=request.user):
                Follower.objects.filter(user=request.data['user'], follower=request.user).delete()
                following=False
            else:
                post_query = Follower.objects.all()
                room_name =''
                follower_serializer = FollowerSerializer(data=request.data)
                if Follower.objects.filter(user=request.user, follower=username):
                    room_name = Follower.objects.get(user=request.user, follower=username).chat_room
                else:
                    room_name = str(request.user) + '_' + str(username)
                    room_name = str(room_name)
                if follower_serializer.is_valid():  
                    follower_serializer.save(chat_room=room_name)
                    following=True

        return Response({"subuser":queryset, "user_profile": user.data['profile'], "img_url": img_url, "posts":user.data['posts'],"following":following, "follower_count":follower_count, "following_count":following_count})

#ChatRoom
def chat_room(request, room_name):
    user_profile = AppUser.objects.get(user=request.user)
    if user_profile.profileImage:
        image_url = user_profile.profileImage.url
    else:
        image_url = ''
    following_list=[]
    followings = Follower.objects.filter(follower=request.user)
    for following in followings:
        following_list.append(following)
    username = str(request.user)
    return render(request, "chat_room.html", {'room_name':room_name, "username":username, 'user_profile':user_profile,'img_url':image_url,'following_list':following_list})


