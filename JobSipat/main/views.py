from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .forms import SignupForm, LoginForm
from .models import Profile
# Create your views here.

def index(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username_or_email = form.cleaned_data['username_or_email']
            password = form.cleaned_data['password']

            user = authenticate(request, username=username_or_email, password=password)

            if user is not None:
                login(request, user)
                profile = request.user.profile
                user_type = profile.user_type

                if user_type == 'Applicant':
                    return redirect('employeeHome')
                elif user_type == 'Employer':
                    return redirect('employeeHome')
                elif user_type == 'Admin':
                    return redirect('employeeHome')
                else:
                    return redirect('index')
            else:
                return render(request, 'main/login.html', {'form': form, 'error': 'Invalid login credentials'})
    else:
        form = LoginForm()

    return render(request, 'main/index.html', {'form': form})


def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            # Create a new User instance
            user = User.objects.create_user(
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password'],
                email=form.cleaned_data['email'],
                first_name=form.cleaned_data['first_name'],
                last_name=form.cleaned_data['last_name'],
            )

            # Create a new Profile instance
            profile = Profile.objects.create(
                user=user,
                phone_number=form.cleaned_data['phone_number'],
                province=form.cleaned_data['province'],
                municipality=form.cleaned_data['municipality'],
                user_type=form.cleaned_data['user_type'],
            )

            # Log the user in
            login(request, user)

            return redirect('index')  # Change 'home' to the desired redirect path after successful signup
    else:
        form = SignupForm()

    return render(request, 'main/Signup.html', {'form': form})


def employeeProfile(response):

    return render(response, "main/employee-profile.html",{})

def employeeNotif(response):
    return render(response, "main/employee-notif.html",{})


def employeeHome(response):

    return render(response, "main/employee-jobs.html",{})

def employeeEdit(response):
    return render(response, "main/employee-edit.html",{})

