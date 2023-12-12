from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .forms import SignupForm, LoginForm, EditForm
from .models import Profile, Job_Post
from django.urls import reverse
from django.http import HttpResponse, JsonResponse
from django.core.mail import send_mail
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt

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
                
                if user_type in ['Applicant', 'Employer', 'Admin']:
                    return redirect(reverse(f'{user_type.lower()}Home'))
                else:
                    return render(request, 'main/index.html', {'form': form, 'error': 'Invalid user type'})
            else:
                return render(request, 'main/index.html', {'form': form, 'error': 'Invalid login credentials'})
    else:
        if request.user.is_authenticated:
            profile = request.user.profile
            user_type = profile.user_type

            if user_type in ['Applicant', 'Employer', 'Admin']:
                return redirect(reverse(f'{user_type.lower()}Home'))
            
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

    return render(request, "main/Applicant/applicant-profile.html", {'user_profile': user_profile})

@login_required
def employeeNotif(request):
    return render(request, "main/Applicant/applicant-notif.html",{})

@login_required
def employeeHome(request):
    job_posts = Job_Post.objects.all()
    user_profile = request.user.profile

    user_skills = user_profile.skills.all() if user_profile else []
    recommended_jobs = Job_Post.objects.filter(skills_recommended__in=user_skills).distinct()

    return render(request, "main/Applicant/applicant-jobs.html", {'job_posts': job_posts, 'recommended_jobs': recommended_jobs})

@csrf_exempt
@login_required
def employeeEdit(request):
    user = request.user
    user_profile = request.user.profile

    if request.method == 'POST':
        form = EditForm(request.POST, request.FILES)  # Include request.FILES in the form instantiation
        if form.is_valid():
            # Update user and user profile fields
            user.first_name = form.cleaned_data['first_name']
            user.last_name = form.cleaned_data['last_name']
            user.email = form.cleaned_data['email']
            user_profile.address = form.cleaned_data['address']
            user_profile.phone_number = form.cleaned_data['phone_number']
            user_profile.birthday = form.cleaned_data['birthday']
            user_profile.age = form.cleaned_data['age']
            user_profile.citizenship = form.cleaned_data['citizenship']
            user_profile.civil_status = form.cleaned_data['civil_status']
            user_profile.sex = form.cleaned_data['gender']
            
            if 'skills' in form.cleaned_data:
                user_profile.skills.set(form.cleaned_data['skills'])
            if 'field_of_expertise' in form.cleaned_data:
                user_profile.field_of_expertise.set(form.cleaned_data['field_of_expertise'])

            if 'resume' in request.FILES:
                user_profile.resume = request.FILES['resume']
            if 'profile_pic' in request.FILES:
                user_profile.profile_pic = request.FILES['profile_pic']

            user.save()
            user_profile.save()
            return redirect('applicantProfile')
        else:
            print(form.errors)
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
            'skills': user_profile.skills.all(),
            'field_of_expertise': user_profile.field_of_expertise.all(),
            'profile_pic': user_profile.profile_pic,
            'resume': user_profile.resume,
        })

    return render(request, "main/Applicant/applicant-edit.html", {'form': form})

@login_required
def applicantViewJob(request, job_post_id):
    job_post = get_object_or_404(Job_Post, id=job_post_id)
    return render(request, "main/Applicant/applicant-view-ad.html", {'job_post': job_post})

def signupPopup(request):
    return render(request,"main/Signup-second.html")

def adminListUser(request):
    return render(request,"main/admin-list-user.html")

def adminListActivity(request):
    return render(request,"main/admin-list-activity.html")

def alertPage(request):
    return render(request,"main/alert-page.html")


