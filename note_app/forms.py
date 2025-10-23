from django import forms
from .models import Notes  # assuming you have a Notes model
from django.contrib.auth.forms import User
from django.contrib.auth.forms import UserCreationForm
class NotesForm(forms.ModelForm):
    class Meta:
        model = Notes
        fields = ['notes', 'description']  # whatever fields your Notes model has


class RegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields=["username","password1","password2"]
        