from django.db import models

# Create your models here.

class Users(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    username = models.CharField(max_length=30, unique=True)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255)  # Store hashed/encrypted password
    contact_number = models.CharField(max_length=15, blank=True, null=True)
    user_types = [
        ('Admin', 'Admin'),
        ('Employee', 'Employee'),
        ('Company', 'Company'),
    ]
    user_type = models.CharField(max_length=10, choices=user_types, default='Employee')
    created_at = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.username