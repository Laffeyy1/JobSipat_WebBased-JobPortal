# Generated by Django 4.2.7 on 2023-12-12 10:07

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0024_job_post_job_application_job_post'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='job_post',
            name='employer',
        ),
        migrations.AddField(
            model_name='job_post',
            name='profile',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='main.profile'),
        ),
    ]