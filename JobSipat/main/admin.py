from django.contrib import admin
from .models import Profile, Skill, Field_of_Expertise, Job_Post, Job_Application, Activity_Logs

# Register your models here.

admin.site.register(Profile)
admin.site.register(Field_of_Expertise)
admin.site.register(Skill)
admin.site.register(Job_Post)
admin.site.register(Job_Application)
admin.site.register(Activity_Logs)