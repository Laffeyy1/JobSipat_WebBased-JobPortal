from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from django.db import models
import os

def user_profile_pic_path(instance, filename):
    return os.path.join('profile', str(instance.user.id), 'profile_pic', filename)

def user_resume_path(instance, filename):
    return os.path.join('profile', str(instance.user.id), 'resume', filename)

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    birthday = models.DateField(null=True, blank=True)
    age = models.IntegerField(null=True, blank=True)
    address = models.CharField(max_length=255, blank=True, default='')
    
    sex_choices = [
        ('Male', 'Male'),
        ('Female', 'Female'),
        ('Other', 'Other'),
    ]
    sex = models.CharField(max_length=10, choices=sex_choices, blank=True, default='')

    current_company = models.CharField(max_length=255, blank=True, default='')
    field_of_expertise = models.ManyToManyField('Field_of_Expertise', blank=True)
    skills = models.ManyToManyField('Skill', blank=True)
    
    civil_status_choices = [
        ('Single', 'Single'),
        ('Married', 'Married'),
        ('Divorced', 'Divorced'),
        ('Widowed', 'Widowed'),
        ('Other', 'Other'),
    ]
    
    civil_status = models.CharField(max_length=10, choices=civil_status_choices, blank=True, default='')

    citizenship = models.CharField(max_length=255, blank=True, default='')
    phone_number = models.IntegerField(blank=True, null=True)
    province = models.CharField(max_length=100, default='')
    municipality = models.CharField(max_length=100, default='')

    user_types = [
        ('Admin', 'Admin'),
        ('Applicant', 'Applicant'),
        ('Employer', 'Employer'),
    ]
    
    user_type = models.CharField(max_length=10, choices=user_types, default='Employee')
    profile_pic = models.ImageField(upload_to=user_profile_pic_path, blank=True, null=True)
    resume = models.FileField(upload_to=user_resume_path, blank=True, null=True)

    def __str__(self):
        return "%s's profile" % self.user.username

class Skill(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name
    
class Field_of_Expertise(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name

class Job_Post(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, null=True, related_name='job_posts')
    title = models.CharField(max_length=255)
    company_name = models.CharField(max_length=255)
    job_position = models.CharField(max_length=255)
    address = models.CharField(max_length=255)

    PART_TIME = 'Part Time'
    FULL_TIME = 'Full Time'
    EMPLOYMENT_TYPE_CHOICES = [
        (PART_TIME, 'Part Time'),
        (FULL_TIME, 'Full Time'),
    ]
    employment_type = models.CharField(
        max_length=20,
        choices=EMPLOYMENT_TYPE_CHOICES,
        default=FULL_TIME,
    )

    salary_offer = models.DecimalField(max_digits=10, decimal_places=2)
    primary_duties = models.TextField()
    job_description = models.TextField()

    field_of_expertise = models.ManyToManyField('Field_of_Expertise', blank=True)
    skills_recommended = models.ManyToManyField('Skill', blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class Job_Application(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=User.objects.first().id)
    job_post = models.ForeignKey(Job_Post, on_delete=models.CASCADE)
    status = models.CharField(max_length=255)
    timestamp = models.DateTimeField(auto_now_add=True)

class Activity_Logs(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    activity = models.CharField(max_length=255)
    timestamp = models.DateTimeField(auto_now_add=True)
    