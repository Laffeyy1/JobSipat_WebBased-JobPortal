from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.

def index(response):
    return render(response, "main/index.html",{})

def signup(response):
    return render(response, "main/Signup.html",{})

def employeeProfile(response):
    return render(response, "main/employee-profile.html",{})

def employeeNotif(response):
    return render(response, "main/employee-notif.html",{})

def employeeJobs(response):
    return render(response, "main/employee-jobs.html",{})

def employeeEdit(response):
    return render(response, "main/employee-edit.html",{})