from django import forms
from .models import *
from django.forms import ModelForm
from django.contrib.auth.models import User

# Form for signup
class UserForm(forms.ModelForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'username', 'class':'register-input'}), label='')
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder':'password', 'class':'register-input'}), label='')
    email = forms.EmailField(widget=forms.TextInput(attrs={'placeholder':'email', 'class':'register-input'}), label='')
    first_name = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'first name', 'class':'register-input'}), label='')
    last_name = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'last name', 'class':'register-input'}), label='')

    class Meta:
        model = User
        fields = ('username', 'password', 'email', 'first_name', 'last_name',)

# Form for signup
class UserProfileForm(forms.ModelForm):
    dateOfBirth = forms.DateField(widget=forms.SelectDateWidget(years=range(1940,2022), attrs={'placeholder':'DOB(mm/dd/yyyy)', 'class':'register-input date-birth'}), label='date of birth')
    profileImage = forms.ImageField(label='profile image', required=False)
    class Meta:
        model = AppUser
        fields = ('dateOfBirth', 'profileImage')

# Forms for user to update their profiles
#First form
class UserFormUpdate(forms.ModelForm):
    email = forms.EmailField(required=False, widget=forms.TextInput(attrs={'class':'profile-update', "id":"profile-update"}), label='email:')
    first_name = forms.CharField(required=False, widget=forms.TextInput(attrs={'class':'profile-update'}), label='first name')
    last_name = forms.CharField(required=False, widget=forms.TextInput(attrs={'class':'profile-update'}), label='last name')

    class Meta:
        model = User
        fields = ('first_name', 'last_name','email')

# Second form
class UserProfileFormUpdate(forms.ModelForm):
    bio = forms.CharField(required=False, widget=forms.Textarea(), label='bio')
    profileImage = forms.ImageField(label='profile image', required=False)
    class Meta:
        model = AppUser
        fields = ('bio', 'profileImage')

#Form to create a new post
class NewPostForm(forms.Form):
    text = forms.CharField(required=True, widget=forms.Textarea(attrs={'placeholder':'what you reckon?'}), label='', help_text="word limit : 500")
    media = forms.ImageField(label="image", required=False)
    user = forms.CharField(widget=forms.HiddenInput(), required=False)

    def save(self, user, time):
        text = self.cleaned_data['text']
        media = self.cleaned_data['media']
        post = Post(user=user, postDate=time, text=text,likes=0, media=media,)
        post.save()