from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Profile,Skill,Field_of_Expertise

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

class EditForm(forms.Form):
    first_name = forms.CharField(widget=forms.TextInput(attrs={
        "class": "info-top",
        "type": "text",
        "placeholder": "First Name"
    }))
    
    last_name = forms.CharField(widget=forms.TextInput(attrs={
        "class": "info-top",
        "type": "text",
        "placeholder": "Last Name"
    }))
    
    address = forms.CharField(widget=forms.TextInput(attrs={
        "class": "info-top",
        "type": "text",
        "placeholder": "No./Street/Barangay/Municipality/Province"
    }))
    
    phone_number = forms.CharField(widget=forms.TextInput(attrs={
        "class": "info-top",
        "type": "text",
        "placeholder": "(000)-0000-0000"
    }))
    
    email = forms.EmailField(widget=forms.TextInput(attrs={
        "class": "info-top",
        "type": "text",
        "placeholder": "@gmail, @yahoo, @hotmail etc."
    }))
    
    birthday = forms.DateField(widget=forms.TextInput(attrs={
        "class": "edit-info1",
        "type": "date",
        "placeholder": "dd/mm/yyyy"
    }))
    
    age = forms.IntegerField(widget=forms.TextInput(attrs={
        "class": "edit-info",
        "type": "text",
        "placeholder": "Years old"
    }))
    
    citizenship = forms.CharField(widget=forms.TextInput(attrs={
        "class": "edit-info",
        "type": "text",
        "placeholder": "ex. Filipino"
    }))
    
    civil_status = forms.ChoiceField(choices=[('Single', 'Single'), ('Married', 'Married'), ('Divorced', 'Divorced'), ('Widowed', 'Widowed'), ('Other', 'Other')],
                                     widget=forms.Select(attrs={"class": "edit-info1"}))
    
    gender = forms.ChoiceField(choices=[('Male', 'Male'), ('Female', 'Female'), ('Other', 'Other')],
                               widget=forms.Select(attrs={"class": "edit-info1"}))
    
    resume = forms.FileField(widget=forms.FileInput(attrs={
        "class": "edit-info",
    }), required=False)

    profile_pic = forms.ImageField(widget=forms.FileInput(attrs={
        "class": "edit-info",
    }), required=False)

    skills = forms.ModelMultipleChoiceField(queryset=Skill.objects.all(), required=True)
    
    field_of_expertise = forms.ModelMultipleChoiceField(queryset=Field_of_Expertise.objects.all(), required=True)
