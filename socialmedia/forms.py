from django import forms
from .models import *
from django.forms import ModelForm
from django.contrib.auth.models import User

# Signup form
class UserForm(forms.ModelForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'username', 'class':'register-input'}), label='')
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder':'password', 'class':'register-input'}), label='')
    email = forms.EmailField(widget=forms.TextInput(attrs={'placeholder':'email', 'class':'register-input'}), label='')
    first_name = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'first name', 'class':'register-input'}), label='')
    last_name = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'last name', 'class':'register-input'}), label='')

    class Meta:
        model = User
        fields = ('username', 'password', 'email', 'first_name', 'last_name',)

# SignUp form Image and DoB
class UserProfileForm(forms.ModelForm):
    dateOfBirth = forms.DateField(widget=forms.SelectDateWidget(years=range(1960,2022), attrs={'placeholder':'DOB(mm/dd/yyyy)', 'class':'register-input date-birth'}), label='DoB')
    profileImage = forms.ImageField(label='Dp', required=False)
    class Meta:
        model = AppUser
        fields = ('dateOfBirth', 'profileImage')

# Update Form
class UserFormUpdate(forms.ModelForm):
    email = forms.EmailField(required=False, widget=forms.TextInput(attrs={'class':'profile-update', "id":"profile-update"}), label='email:')
    first_name = forms.CharField(required=False, widget=forms.TextInput(attrs={'class':'profile-update'}), label='first name')
    last_name = forms.CharField(required=False, widget=forms.TextInput(attrs={'class':'profile-update'}), label='last name')

    class Meta:
        model = User
        fields = ('first_name', 'last_name','email')

class UserProfileFormUpdate(forms.ModelForm):
    bio = forms.CharField(required=False, widget=forms.Textarea(), label='bio')
    profileImage = forms.ImageField(label='profile image', required=False)
    class Meta:
        model = AppUser
        fields = ('bio', 'profileImage')

#Newpost Form
class NewPostForm(forms.Form):
    text = forms.CharField(required=True, widget=forms.Textarea(attrs={'placeholder':'Write your thoughts'}), label='', help_text="Limit : 250")
    media = forms.ImageField(label="image", required=False)
    user = forms.CharField(widget=forms.HiddenInput(), required=False)

    def save(self, user, time):
        text = self.cleaned_data['text']
        media = self.cleaned_data['media']
        post = Post(user=user, postDate=time, text=text,likes=0, media=media,)
        post.save()
