from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Profile

class UserRegistrationForm(UserCreationForm):
    email=forms.EmailField(widget=forms.TextInput(attrs={'style': 'width:90%'}))
    username=forms.CharField(max_length=200, widget=forms.TextInput(attrs={'style': 'width:90%'}),)
    first_name=forms.CharField(max_length=200, widget=forms.TextInput(attrs={'style': 'width:90%'}),)
    last_name=forms.CharField(max_length=200, widget=forms.TextInput(attrs={'style': 'width:90%'}),)
    password1=forms.CharField(max_length=200, widget=forms.TextInput(attrs={'style': 'width:90%'}),)
    password2=forms.CharField(max_length=200, widget=forms.TextInput(attrs={'style': 'width:90%'}),)
    class Meta:
        model=User
        fields=['username', 'email', 'first_name', 'last_name','password1','password2']

class UserUpdateForm(forms.ModelForm):
    email=forms.EmailField()
    class Meta:
        model = User
        fields = ['username', 'email']

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['image','bio']