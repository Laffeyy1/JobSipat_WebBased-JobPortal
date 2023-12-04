from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from django.db import models

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_number = models.IntegerField(blank=True, null=True)
    province = models.CharField(max_length=100, default='')
    municipality = models.CharField(max_length=100, default='')
    user_types = [
        ('Admin', 'Admin'),
        ('Applicant', 'Applicant'),
        ('Employer', 'Employer'),
    ]
    user_type = models.CharField(max_length=10, choices=user_types, default='Employee')

    def __str__(self):
        return "%s's profile" % self.user.username