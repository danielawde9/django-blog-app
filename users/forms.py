from django import forms
from django.contrib.auth.forms import UserChangeForm, UserCreationForm

from .models import CustomUser

class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = CustomUser
        # default forms - fields = UserCreationForm.Meta.fields + ('age',)
        fields = ('username', 'email', 'age',) # new after fixing the templates

class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = CustomUser
        # default forms - fields = UserChangeForm.Meta.fields
        fields = ('username', 'email', 'age',) 