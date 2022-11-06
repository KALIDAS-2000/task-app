
from django.contrib.auth.models import User
from django import forms
from task.models import Task


class RegistrationForms(forms.ModelForm):
    class Meta:
        model=User
        fields=['first_name','last_name','username','email','password']
        widgets={
            "first_name":forms.TextInput(attrs={"class":"form-control border border-primary placeholder col-12 bg-primary"}),
            "last_name":forms.TextInput(attrs={"class":"form-control border border-primary placeholder col-12 bg-primary"}),
            "username":forms.TextInput(attrs={"class":"form-control border border-primary placeholder col-12 bg-primary"}),
            "email":forms.EmailInput(attrs={"class":"form-control border border-primary placeholder col-12 bg-primary"}),
            "password":forms.PasswordInput(attrs={"class":"form-control border border-primary placeholder col-12 bg-primary"}),
        }

class LoginForm(forms.Form):
    username=forms.CharField(widget=forms.TextInput(attrs={'class':"form-control border border-primary"}))
    password=forms.CharField(widget=forms.PasswordInput(attrs={'class':"form-control border border-primary"}))


class TaskUpdateForm(forms.ModelForm):
    class Meta:
        model=Task
        fields=['task_name',"status"]