import datetime

from django.db import models
from django.utils import timezone
from django import forms 
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User

class Message(models.Model):
    message_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')

    def __str__(self):
        return self.message_text

class SignupForm(UserCreationForm):
    class Meta:
        model = User 
        fields = ['username', 'password1', 'password2']

class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['message_text', 'pub_date']
        widgets = {
            'pub_date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }