from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .forms import SignupForm, LoginForm, EditForm, JobSearchForm, JobPostForm
from .models import Profile, Job_Post
from django.urls import reverse
from django.http import HttpResponse, JsonResponse
from django.core.mail import send_mail
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
from django.db.models import Q

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
def applicantProfile(request):
    user_profile = None
    if hasattr(request.user, 'profile'):
        user_profile = request.user.profile
    else:
        print("No profile found for user:", request.user)

    return render(request, "main/Applicant/applicant-profile.html", {'user_profile': user_profile})

@login_required
def applicantNotif(request):
    return render(request, "main/Applicant/applicant-notif.html",{})

@login_required
def applicantHome(request):
    # Get all job posts
    job_posts = Job_Post.objects.all().order_by('-created_at')

    # Get the user's profile
    user_profile = getattr(request.user, 'profile', None)
    # Get the user's skills
    user_skills = user_profile.skills.all() if user_profile else []

    # Get recommended jobs based on user skills
    recommended_jobs = Job_Post.objects.filter(skills_recommended__in=user_skills).distinct()

    # Handle search parameters
    form = JobSearchForm(request.GET)
    if form.is_valid():
        job_title = form.cleaned_data['job_title']
        skills = form.cleaned_data['skills']
        city = form.cleaned_data['city']
        country = form.cleaned_data['country']

        filtered_job_posts = job_posts

        if job_title:
            filtered_job_posts = filtered_job_posts.filter(title__icontains=job_title)

        if skills:
            filtered_job_posts = filtered_job_posts.filter(skills_recommended__name__icontains=skills)

        if city:
            filtered_job_posts = filtered_job_posts.filter(address__icontains=city)

        if country:
            filtered_job_posts = filtered_job_posts.filter(address__icontains=country)
    else:
        filtered_job_posts = job_posts

    return render(request, "main/Employer/employer-job-offers.html", {
        'job_posts': filtered_job_posts,
        'recommended_jobs': recommended_jobs,
        'form': form,
    })

@csrf_exempt
@login_required
def applicantEdit(request):
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

@login_required
def employerHome(request):
    # Get all job posts
    job_posts = Job_Post.objects.all().order_by('-created_at')

    # Get the user's profile
    user_profile = getattr(request.user, 'profile', None)

    # Get the user's skills
    user_skills = user_profile.skills.all() if user_profile else []

    # Get recommended jobs based on user skills
    recommended_jobs = Job_Post.objects.filter(skills_recommended__in=user_skills).distinct()

    # Handle search parameters
    form = JobSearchForm(request.GET)
    if form.is_valid():
        job_title = form.cleaned_data['job_title']
        skills = form.cleaned_data['skills']
        city = form.cleaned_data['city']
        country = form.cleaned_data['country']

        filtered_job_posts = job_posts

        if job_title:
            filtered_job_posts = filtered_job_posts.filter(title__icontains=job_title)

        if skills:
            filtered_job_posts = filtered_job_posts.filter(skills_recommended__name__icontains=skills)

        if city:
            filtered_job_posts = filtered_job_posts.filter(address__icontains=city)

        if country:
            filtered_job_posts = filtered_job_posts.filter(address__icontains=country)
    else:
        filtered_job_posts = job_posts

    return render(request, "main/Employer/employer-job-offers.html", {
        'job_posts': filtered_job_posts,
        'recommended_jobs': recommended_jobs,
        'form': form,
    })

@login_required
def employerPostAd(request):
    if request.method == 'POST':
        form = JobPostForm(request.POST)
        if form.is_valid():
            job_post = form.save()

            # Get profiles with similar skills
            similar_profiles = Profile.objects.filter(
                Q(skills__in=job_post.skills_recommended.all()) |
                Q(field_of_expertise__in=job_post.field_of_expertise.all())
            ).exclude(user=request.user).distinct()

            # Send emails to the users with similar skills
            for profile in similar_profiles:
                send_mail(
                    'New Job Opportunity',
                    f'Hello {profile.user.username},\n\n'
                    f'There is a new job opportunity that matches your skills. Check it out on our platform!',
                    settings.EMAIL_HOST_USER,
                    [profile.user.email],
                    fail_silently=False
                )

            return redirect('employerHome')
    else:
        form = JobPostForm()

    return render(request, 'main/Employer/employer-post-ad.html', {'form': form})

@login_required
def employerPostEdit(request, job_post_id):
    # Get the existing job post
    job_post = get_object_or_404(Job_Post, id=job_post_id)

    if request.method == 'POST':
        form = JobPostForm(request.POST, instance=job_post)
        if form.is_valid():
            form.save()
            return redirect('employerHome')
    else:
        form = JobPostForm(instance=job_post)

    return render(request, 'main/Employer/employer-post-edit.html', {'form': form})

def employerProfile(request):
    return render(request,"main/Employer/employer-profile.html")

def employerEdit(request):
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
    return render(request,"main/Employer/employer-edit.html", {'form': form})

def signupPopup(request):
    return render(request,"main/Signup-second.html")

def adminListUser(request):
    return render(request,"main/admin-list-user.html")

def adminListActivity(request):
    return render(request,"main/admin-list-activity.html")

def alertPage(request):
    return render(request,"main/alert-page.html")


