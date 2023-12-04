from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class LoginForm(forms.Form):
    username_or_email = forms.CharField(widget=forms.TextInput(attrs={
        "class": "info",
        "type": "text",
        "placeholder": "Username / Email",
    }), label="")

    password = forms.CharField(widget=forms.PasswordInput(attrs={
        "class": "info",
        "type": "password",
        "placeholder": "Password",
    }), label="")

class SignupForm(forms.Form):
    first_name = forms.CharField(widget=forms.TextInput(attrs={
        "class": "name",
        "type": "text",
        "placeholder": "First Name"
    }))
    
    last_name = forms.CharField(widget=forms.TextInput(attrs={
        "class": "name",
        "type": "text",
        "placeholder": "Last Name"
    }))
    
    username = forms.CharField(max_length=30, widget=forms.TextInput(attrs={
        "class": "name",
        "type": "text",
        "placeholder": "Username"
    }))
    
    email = forms.EmailField(widget=forms.TextInput(attrs={
        "class": "email",
        "type": "text",
        "placeholder": "Email"
    }))
    
    phone_number = forms.CharField(max_length=11, widget=forms.TextInput(attrs={
        "class": "number",
        "type": "text",
        "placeholder": "+63*********"
    }))
    
    province = forms.CharField(widget=forms.Select(attrs={
        "class": "loc-derma",
        "id": "province",
    }))
    
    municipality = forms.CharField(widget=forms.Select(attrs={
        "class": "loc-derma",
        "id": "city",
    }))
    
    user_type = forms.ChoiceField(choices=[('Applicant', 'Applicant'), ('Employer', 'Employer')], widget=forms.Select(attrs={
        "class": "user-derma"
    }))
    
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        "class": "pass",
        "type": "password",
        "placeholder": "Password"
    }))
    
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={
        "class": "confirm",
        "type": "password",
        "placeholder": "Confirm Password"
    }))