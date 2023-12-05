# Generated by Django 4.2.7 on 2023-12-04 11:58

from django.db import migrations, models
import main.models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0008_profile_age_profile_citizenship_profile_civil_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='profile_pic',
            field=models.ImageField(blank=True, null=True, upload_to=main.models.user_profile_pic_path),
        ),
        migrations.AddField(
            model_name='profile',
            name='resume',
            field=models.FileField(blank=True, null=True, upload_to=main.models.user_resume_path),
        ),
    ]