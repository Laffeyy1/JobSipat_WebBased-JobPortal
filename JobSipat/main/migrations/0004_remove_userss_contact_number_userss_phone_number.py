# Generated by Django 4.2.7 on 2023-12-03 13:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0003_userss_municipality_userss_province_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userss',
            name='contact_number',
        ),
        migrations.AddField(
            model_name='userss',
            name='phone_number',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
