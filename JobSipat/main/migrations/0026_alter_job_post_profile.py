# Generated by Django 4.2.7 on 2023-12-12 10:12

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0025_remove_job_post_employer_job_post_profile'),
    ]

    operations = [
        migrations.AlterField(
            model_name='job_post',
            name='profile',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='job_posts', to='main.profile'),
        ),
    ]
