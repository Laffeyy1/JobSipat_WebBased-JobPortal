# Generated by Django 4.2.7 on 2023-12-12 09:38

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0015_alter_job_post_profile'),
    ]

    operations = [
        migrations.AlterField(
            model_name='job_post',
            name='profile',
            field=models.OneToOneField(default=2, on_delete=django.db.models.deletion.CASCADE, to='main.profile'),
        ),
    ]