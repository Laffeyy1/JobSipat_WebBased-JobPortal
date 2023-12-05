# Generated by Django 4.2.7 on 2023-12-05 14:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0009_profile_profile_pic_profile_resume'),
    ]

    operations = [
        migrations.CreateModel(
            name='Job_Post',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('company_name', models.CharField(max_length=255)),
                ('job_position', models.CharField(max_length=255)),
                ('address', models.CharField(max_length=255)),
                ('employment_type', models.CharField(choices=[('Part Time', 'Part Time'), ('Full Time', 'Full Time')], default='Full Time', max_length=20)),
                ('salary_offer', models.DecimalField(decimal_places=2, max_digits=10)),
                ('primary_duties', models.TextField()),
                ('job_description', models.TextField()),
                ('skills_recommended', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]