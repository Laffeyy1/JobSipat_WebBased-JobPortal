from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.hashers import check_password, make_password
from .forms import LoginForm, SignupForm
from .models import Userss
from django.db.models import Q

# Create your views here.

def index(response):
    if response.method == 'POST':
        form = LoginForm(response.POST)
        if form.is_valid():
            username_or_email = form.cleaned_data['username_or_email']
            password = form.cleaned_data['password']
            
            user = Userss.objects.filter(Q(username=username_or_email) | Q(email=username_or_email)).first()

            if user and check_password(password, user.password):
                print("Redirecting to home...")
                return redirect('home')
            else:
                print("Authentication failed.")
                pass
    else:
        form = LoginForm()

    return render(response, 'main/index.html', {'form': form})

def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            phone_number = int(form.cleaned_data['phone_number'])
            province = form.cleaned_data['province']
            municipality = form.cleaned_data['municipality']
            user_type = form.cleaned_data['user_type']
            password = form.cleaned_data['password']
            confirm_password = form.cleaned_data['confirm_password']

            # Check if passwords match
            if password == confirm_password:
                # Create a new user instance and save it to the database
                user = Userss(
                    first_name=first_name,
                    last_name=last_name,
                    username=username,
                    email=email,
                    phone_number=phone_number,
                    province=province,
                    municipality=municipality,
                    user_type=user_type,
                    password=make_password(password),  # Hash the password before saving
                )
                user.save()

                # Redirect to a success page or login page
                return redirect('home')  # Change 'success' to the appropriate URL name

    else:
        form = SignupForm()

    return render(request, 'main/Signup.html', {'form': form})

def employeeProfile(response):
    return render(response, "main/employee-profile.html",{})

def employeeNotif(response):
    return render(response, "main/employee-notif.html",{})

def home(response):
    return render(response, "main/employee-jobs.html",{})

def employeeEdit(response):
    return render(response, "main/employee-edit.html",{})