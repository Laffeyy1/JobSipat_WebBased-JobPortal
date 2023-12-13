from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Profile,Skill,Field_of_Expertise, Job_Post

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

class JobSearchForm(forms.Form):
    job_title = forms.CharField(required=False, widget=forms.TextInput(attrs={'placeholder': 'Job Title'}))
    skills = forms.CharField(required=False, widget=forms.TextInput(attrs={'placeholder': 'Skills'}))
    city = forms.CharField(required=False, widget=forms.TextInput(attrs={'placeholder': 'City'}))
    country = forms.CharField(required=False, widget=forms.TextInput(attrs={'placeholder': 'Country'}))

class JobPostForm(forms.ModelForm):
    
    field_of_expertise = forms.ModelMultipleChoiceField(
        queryset=Field_of_Expertise.objects.all(),  # Replace with the actual queryset
        widget=forms.CheckboxSelectMultiple,
        required=False
    )

    skills_recommended = forms.ModelMultipleChoiceField(
        queryset=Skill.objects.all(),  # Replace with the actual queryset
        widget=forms.CheckboxSelectMultiple,
        required=False
    )

    class Meta:
        model = Job_Post
        fields = ['title', 'company_name', 'job_position', 'address', 'employment_type', 'salary_offer', 'primary_duties', 'job_description', 'field_of_expertise', 'skills_recommended']

    widgets = {
        'title': forms.TextInput(attrs={'placeholder': 'Enter job title'}),
        'company_name': forms.TextInput(attrs={'placeholder': 'Enter company name'}),
        'job_position': forms.TextInput(attrs={'placeholder': 'Enter job position'}),
        'address': forms.TextInput(attrs={'placeholder': 'Enter address'}),
        'salary_offer': forms.TextInput(attrs={'placeholder': 'Enter salary offer'}),
        'primary_duties': forms.Textarea(attrs={'placeholder': 'Enter primary duties and responsibilities'}),
        'job_description': forms.Textarea(attrs={'placeholder': 'Enter job description'}),
    }

class EditUserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']
        widgets = {
            'first_name': forms.TextInput(attrs={
                "class": "info-top",
                "type": "text",
                "placeholder": "First Name"
            }),
            'last_name': forms.TextInput(attrs={
                "class": "info-top",
                "type": "text",
                "placeholder": "Last Name"
            }),
            'email': forms.EmailInput(attrs={
                "class": "info-top",
                "type": "text",
                "placeholder": "@gmail, @yahoo, @hotmail etc."
            }),
        }
class EditProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['birthday', 'age', 'address', 'sex', 'current_company', 'field_of_expertise', 'skills', 'civil_status', 'citizenship', 'phone_number', 'province', 'municipality', 'user_type', 'profile_pic', 'resume']
        widgets = {
            'birthday': forms.TextInput(attrs={
                "class": "edit-info1",
                "type": "date",
                "placeholder": "dd/mm/yyyy"
            }),
            'age': forms.TextInput(attrs={
                "class": "edit-info",
                "type": "text",
                "placeholder": "Years old"
            }),
            'address': forms.TextInput(attrs={
                "class": "edit-info",
                "type": "text",
                "placeholder": "Street, Block, City"
            }),
            'citizenship': forms.TextInput(attrs={
                "class": "edit-info",
                "type": "text",
                "placeholder": "ex. Filipino"
            }),
            'phone_number': forms.TextInput(attrs={
                "class": "edit-info",
                "type": "text",
                "placeholder": "ex. Filipino"
            }),
            'civil_status': forms.Select(attrs={"class": "edit-info1"}),
            'sex': forms.Select(attrs={"class": "edit-info1"}),
            'profile_pic': forms.FileInput(attrs={
                "class": "edit-info",
            }),
            'resume': forms.FileInput(attrs={
                "class": "edit-info",
            }),
        }