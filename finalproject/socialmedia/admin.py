from django.contrib import admin
from .models import *

# Register your models here.
class AppUserAdmin(admin.ModelAdmin):
    list_display=('user', 'profileImage', 'dateOfBirth', 'bio')

class PostAdmin(admin.ModelAdmin):
    list_display=('postId', 'user', 'postDate', 'text', 'likes', 'media')

class FollowerAdmin(admin.ModelAdmin):
    list_display=('user', 'follower', 'chat_room')

admin.site.register(AppUser, AppUserAdmin)
admin.site.register(Post, PostAdmin)
admin.site.register(Follower, FollowerAdmin)