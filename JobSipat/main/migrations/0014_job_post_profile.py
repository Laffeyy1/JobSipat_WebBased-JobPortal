# Generated by Django 4.2.7 on 2023-12-12 09:36

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('main', '0013_field_of_expertise_remove_profile_field_of_expertise_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='job_post',
            name='profile',
            field=models.OneToOneField(default=1, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
