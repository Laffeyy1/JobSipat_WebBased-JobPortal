from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .forms import SignupForm, LoginForm, EditForm
from .models import Profile, Job_Post
from django.http import HttpResponse

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
                return render(request, 'main/index.html', {'form': form, 'error': 'Invalid login credentials'})
    else:
        if request.user.is_authenticated:
            profile = request.user.profile
            user_type = profile.user_type

            if user_type == 'Applicant':
                return redirect('employeeHome')
            elif user_type == 'Employer':
                return redirect('employerHome')
            elif user_type == 'Admin':
                return redirect('adminHome')
            
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

            return redirect('index')
    else:
        form = SignupForm()

    return render(request, 'main/Signup.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('index')

@login_required
def employeeProfile(request):
    user_profile = None
    if hasattr(request.user, 'profile'):
        user_profile = request.user.profile
    else:
        print("No profile found for user:", request.user)

    return render(request, "main/employee-profile.html", {'user_profile': user_profile})

@login_required
def employeeNotif(request):
    return render(request, "main/employee-notif.html",{})

@login_required
def employeeHome(request):
    job_posts = Job_Post.objects.all()
    user_profile = None
    if hasattr(request.user, 'profile'):
        user_profile = request.user.profile
    else:
        print("No profile found for user:", request.user)

    return render(request, "main/employee-jobs.html", {'job_posts': job_posts})

@login_required
def employeeEdit(request):
    user = request.user
    user_profile = request.user.profile
    if request.method == 'POST':
        form = EditForm(request.POST)
        if form.is_valid():
            user.first_name = form.cleaned_data['first_name']
            user.last_name = form.cleaned_data['last_name']
            user.email = form.cleaned_data['email']
            user_profile = user.profile
            user_profile.address = form.cleaned_data['address']
            user_profile.phone_number = form.cleaned_data['phone_number']
            user_profile.birthday = form.cleaned_data['birthday']
            user_profile.age = form.cleaned_data['age']
            user_profile.citizenship = form.cleaned_data['citizenship']
            user_profile.civil_status = form.cleaned_data['civil_status']
            user_profile.sex = form.cleaned_data['gender']
            user_profile.skills = form.cleaned_data['skills']
            user_profile.field_of_expertise = form.cleaned_data['field_of_expertise']

            if 'resume' in request.FILES:
                user_profile.resume = request.FILES['resume']
            if 'profile_pic' in request.FILES:
                user_profile.profile_pic = request.FILES['profile_pic']


            user.save()
            user_profile.save()
            return redirect('employeeProfile')
    else:

        form = EditForm(initial={
            'first_name': user.first_name,
            'last_name': user.last_name,
            'email': user.email,
            'address': user_profile.address,
            'phone_number': user_profile.phone_number,
            'birthday': user_profile.birthday,
            'age': user_profile.age,
            'citizenship': user_profile.citizenship,
            'civil_status': user_profile.civil_status,
            'gender': user_profile.sex,
            'skills': user_profile.skills,
            'field_of_expertise': user_profile.field_of_expertise,
            'profile_pic' : user_profile.profile_pic,
            'resume' : user_profile.resume,
        })

    return render(request, "main/employee-edit.html", {'form': form})