# Generated by Django 4.2.7 on 2023-12-12 09:39

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0016_alter_job_post_profile'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='job_post',
            name='profile',
        ),
    ]
