from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .forms import SignupForm, LoginForm, EditForm, JobSearchForm, JobPostForm, EditUserForm, EditProfileForm
from .models import Profile, Job_Post, Notifications, Job_Application, Activity_Logs
from django.urls import reverse
from django.http import HttpResponse, JsonResponse
from django.core.mail import send_mail
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
from django.db.models import Q, Count
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph
from reportlab.lib.styles import getSampleStyleSheet
from io import BytesIO
from reportlab.lib import colors
from datetime import datetime, timedelta
from django.utils import timezone
from django.contrib.auth.decorators import user_passes_test

# Create your views here.

def is_applicant(user):
    return user.profile.user_type == 'Applicant' if hasattr(user, 'profile') else False

def is_employer(user):
    return user.profile.user_type == 'Employer' if hasattr(user, 'profile') else False

def is_admin(user):
    return user.profile.user_type == 'Admin' if hasattr(user, 'profile') else False


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

                log_activity(request, "Logged In")
                
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

            log_activity(request, "Logged In")

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
    log_activity(request, "Logged Out")
    logout(request)
    return redirect('index')

@login_required
@user_passes_test(is_applicant, login_url='/unauthorized_access/')
def applicantProfile(request):
    user_profile = None
    unread_notification_count = Notifications.objects.filter(user=request.user, read=False).count()
    if hasattr(request.user, 'profile'):
        user_profile = request.user.profile
    else:
        print("No profile found for user:", request.user)

    return render(request, "main/Applicant/applicant-profile.html", {'user_profile': user_profile, 'unread_notification_count': unread_notification_count})

@login_required
@user_passes_test(is_applicant, login_url='/unauthorized_access/')
def applicantNotif(request):
    unread_notification_count = Notifications.objects.filter(user=request.user, read=False).count()

    return render(request, "main/Applicant/applicant-notif.html",{'unread_notification_count': unread_notification_count})

@login_required
@user_passes_test(is_applicant, login_url='/unauthorized_access/')
def applicantHome(request):
    # Get all job posts
    job_posts = Job_Post.objects.all().order_by('-created_at')

    # Get the user's profile
    user_profile = getattr(request.user, 'profile', None)
    # Get the user's skills
    user_skills = user_profile.skills.all() if user_profile else []

    # Get recommended jobs based on user skills
    recommended_jobs = Job_Post.objects.filter(skills_recommended__in=user_skills).distinct()

    unread_notification_count = Notifications.objects.filter(user=request.user, read=False).count()
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

    return render(request, "main/Applicant/applicant-jobs.html", {
        'job_posts': filtered_job_posts,
        'recommended_jobs': recommended_jobs,
        'form': form,
        'unread_notification_count': unread_notification_count
    })

@csrf_exempt
@login_required
@user_passes_test(is_applicant, login_url='/unauthorized_access/')
def applicantEdit(request):
    user = request.user
    user_profile = request.user.profile
    unread_notification_count = Notifications.objects.filter(user=request.user, read=False).count()
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

    return render(request, "main/Applicant/applicant-edit.html", {'form': form, 'unread_notification_count': unread_notification_count})

@login_required
@user_passes_test(is_applicant, login_url='/unauthorized_access/')
def applicantViewJob(request, job_post_id):
    job_post = get_object_or_404(Job_Post, id=job_post_id)
    user = request.user

    # Check if the user has already applied for this job
    application = Job_Application.objects.filter(user=user, job_post=job_post).first()

    if application:
        # User has already applied, display the current status
        current_status = application.get_status_display()
    else:
        # User has not applied, handle form submission
        if request.method == 'POST':
            # Create a new Job_Application instance
            Job_Application.objects.create(user=user, job_post=job_post)

            # Redirect to the same page to avoid form resubmission
            return redirect('applicant-view-job', job_post_id=job_post.id)

        current_status = None

    # Count unread notifications for the current user
    unread_notification_count = Notifications.objects.filter(user=user, read=False).count()

    return render(
        request,
        "main/Applicant/applicant-view-ad.html",
        {
            'job_post': job_post,
            'unread_notification_count': unread_notification_count,
            'current_status': current_status,
        }
    )

@login_required
@user_passes_test(is_employer, login_url='/unauthorized_access/')
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
@user_passes_test(is_employer, login_url='/unauthorized_access/')
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
                # Create notification entries for users with similar skills
                notification_text = f'There is a new job opportunity that matches your skills. Check it out on our platform!'
                Notifications.objects.create(user=profile.user, notification=notification_text)

                # Send emails if needed
                send_mail(
                    'New Job Opportunity',
                    notification_text,
                    settings.EMAIL_HOST_USER,
                    [profile.user.email],
                    fail_silently=False
                )

            return redirect('employerHome')
    else:
        form = JobPostForm()

    return render(request, 'main/Employer/employer-post-ad.html', {'form': form})

@login_required
@user_passes_test(is_employer, login_url='/unauthorized_access/')
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

@login_required
@user_passes_test(is_employer, login_url='/unauthorized_access/')
def employerProfile(request):
    user_profile = None
    if hasattr(request.user, 'profile'):
        user_profile = request.user.profile
    else:
        print("No profile found for user:", request.user)

    return render(request,"main/Employer/employer-profile.html", {'user_profile': user_profile})

@login_required
@user_passes_test(is_employer, login_url='/unauthorized_access/')
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

@login_required
@user_passes_test(is_admin, login_url='/unauthorized_access/')
def adminHome(request):
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

        sort_by = request.GET.get('sort_by')
        if sort_by == 'Daily':
            job_posts = job_posts.filter(created_at__gte=timezone.now() - timedelta(days=1))
        elif sort_by == 'Weekly':
            job_posts = job_posts.filter(created_at__gte=timezone.now() - timedelta(weeks=1))
        elif sort_by == 'Monthly':
            job_posts = job_posts.filter(created_at__gte=timezone.now() - timedelta(weeks=4))
    else:
        filtered_job_posts = job_posts



    return render(request, "main/Admin/admin-jobs.html", {
        'job_posts': filtered_job_posts,
        'recommended_jobs': recommended_jobs,
        'form': form,
    })

@login_required
@user_passes_test(is_admin, login_url='/unauthorized_access/')
def adminListUser(request):
    users = Profile.objects.all()
    return render(request, "main/Admin/admin-list-user.html", {'users': users})

@login_required
@user_passes_test(is_admin, login_url='/unauthorized_access/')
def edit_user(request, user_id):
    user_profile = get_object_or_404(Profile, user__id=user_id)

    if request.method == 'POST':
        user_form = EditUserForm(request.POST, instance=user_profile.user)
        profile_form = EditProfileForm(request.POST, request.FILES, instance=user_profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            log_activity(request, "Edit User")
            return redirect('adminListUser')  # Adjust the URL as needed
    else:
        user_form = EditUserForm(instance=user_profile.user)
        profile_form = EditProfileForm(instance=user_profile)

    return render(request, 'main/Admin/admin-edit-user.html', {'user_profile': user_profile, 'user_form': user_form, 'profile_form': profile_form})

@login_required
@user_passes_test(is_admin, login_url='/unauthorized_access/')
def delete_user(request, user_id):
    user = get_object_or_404(Profile, user__id=user_id)
    user.user.delete()
    log_activity(request, "User Deleted")
    return redirect('adminListUser')

@login_required
@user_passes_test(is_admin, login_url='/unauthorized_access/')
def create_user(request):
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
            log_activity(request, "Created A User")
            return redirect('adminListUser')
    else:
        form = SignupForm()

    return render(request, 'main/Admin/admin-create-user.html', {'form': form})

@login_required
@user_passes_test(is_admin, login_url='/unauthorized_access/')
def user_generate_pdf_report(request):
    profiles = Profile.objects.all()
    buffer = BytesIO()

    # Create the PDF object, using the BytesIO object as its "file."
    pdf = SimpleDocTemplate(buffer, pagesize=letter)

    # Create a list to hold all elements in the PDF
    elements = []

    # Add a title to the PDF
    elements.append(pdf.para(paraText="User Report", style='Title'))

    report_status = "This report provides information about users."
    elements.append(Paragraph(report_status))

    # Define the table data
    data = [['ID', 'Username', 'Email', 'User Type']]

    # Add data rows
    for i, profile in enumerate(profiles):
        user = profile.user  # Assuming a one-to-one relationship
        data.append([i + 1, user.username, user.email, profile.user_type])

    # Create the table
    table = Table(data, colWidths=[50, 150, 150, 100])

    # Add style to the table
    style = TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ])
    table.setStyle(style)

    # Add the table to the elements list
    elements.append(table)

    # Build the PDF
    pdf.build(elements)

    # File is now complete.
    buffer.seek(0)

    # Create a response object.
    response = HttpResponse(content_type="application/pdf")
    response["Content-Disposition"] = 'attachment; filename="user_report.pdf"'

    # Write the PDF to the response.
    response.write(buffer.read())

    return response

@login_required
@user_passes_test(is_admin, login_url='/unauthorized_access/')
def user_generate_pdf_report_view(request):
    profiles = Profile.objects.all()
    buffer = BytesIO()

    pdf_title = "User Report"
    pdf_title_with_date = f"{pdf_title} - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"

    pdf = SimpleDocTemplate(buffer, pagesize=letter, title=pdf_title_with_date)

    elements = []

    styles = getSampleStyleSheet()
    elements.append(Paragraph("User Report", styles['Title']))

    report_status = "This report provides information about users."
    elements.append(Paragraph(report_status))

    # Define the table data
    data = [['ID', 'Username', 'Email', 'User Type']]

    # Add data rows
    for i, profile in enumerate(profiles):
        user = profile.user  # Assuming a one-to-one relationship
        data.append([i + 1, user.username, user.email, profile.user_type])

    table = Table(data, colWidths=[50, 150, 150, 100])

    style = TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.white),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ])
    table.setStyle(style)

    elements.append(table)

    pdf.build(elements)

    buffer.seek(0)

    response = HttpResponse(content_type="application/pdf")
    response["Content-Disposition"] = 'inline; filename="user_report.pdf"'

    response.write(buffer.read())

    return response

@login_required
@user_passes_test(is_admin, login_url='/unauthorized_access/')
def job_generate_pdf_report_view(request):
    job_posts = Job_Post.objects.all()
    buffer = BytesIO()

    pdf_title = "Job Report"
    pdf_title_with_date = f"{pdf_title} - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
    # Create the PDF object, using the BytesIO object as its "file."
    pdf = SimpleDocTemplate(buffer, pagesize=letter, title=pdf_title_with_date)

    # Create a list to hold all elements in the PDF
    elements = []

    # Add a title to the PDF
    elements.append(Paragraph("Job Post Report", getSampleStyleSheet()['Title']))

    report_status = "This report provides information about job posts."
    elements.append(Paragraph(report_status, getSampleStyleSheet()['BodyText']))

    # Define the table data
    data = [['ID', 'Title', 'Company', 'Address', 'Employment Type', 'Salary']]

    # Add data rows
    for i, job_post in enumerate(job_posts):
        data.append([
            i + 1,
            job_post.title,
            job_post.company_name,
            job_post.address,
            job_post.get_employment_type_display(),  # Get display value for choices field
            job_post.salary_offer,
        ])

    # Create the table
    table = Table(data, colWidths=[30, 150, 100, 150, 80, 80])

    # Add style to the table
    style = TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 9),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ])
    table.setStyle(style)

    # Add the table to the elements list
    elements.append(table)

    # Build the PDF
    pdf.build(elements)

    # File is now complete.
    buffer.seek(0)

    # Create a response object.
    response = HttpResponse(content_type="application/pdf")
    response["Content-Disposition"] = 'filename="job_post_report.pdf"'

    # Write the PDF to the response.
    response.write(buffer.read())

    return response

@login_required
@user_passes_test(is_admin, login_url='/unauthorized_access/')
def job_generate_pdf_report(request):
    log_activity(request, "PDF Generate Job")
    job_posts = Job_Post.objects.all()
    buffer = BytesIO()

    pdf_title = "Job Report"
    pdf_title_with_date = f"{pdf_title} - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
    # Create the PDF object, using the BytesIO object as its "file."
    pdf = SimpleDocTemplate(buffer, pagesize=letter, title=pdf_title_with_date)

    # Create a list to hold all elements in the PDF
    elements = []

    # Add a title to the PDF
    elements.append(Paragraph("Job Post Report", getSampleStyleSheet()['Title']))

    report_status = "This report provides information about job posts."
    elements.append(Paragraph(report_status, getSampleStyleSheet()['BodyText']))

    # Define the table data
    data = [['ID', 'Title', 'Company', 'Address', 'Employment Type', 'Salary']]

    # Add data rows
    for i, job_post in enumerate(job_posts):
        data.append([
            i + 1,
            job_post.title,
            job_post.company_name,
            job_post.address,
            job_post.get_employment_type_display(),  # Get display value for choices field
            job_post.salary_offer,
        ])

    # Create the table
    table = Table(data, colWidths=[30, 150, 150, 150, 80, 80])

    # Add style to the table
    style = TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ])
    table.setStyle(style)

    # Add the table to the elements list
    elements.append(table)

    # Build the PDF
    pdf.build(elements)

    # File is now complete.
    buffer.seek(0)

    # Create a response object.
    response = HttpResponse(content_type="application/pdf")
    response["Content-Disposition"] = 'attachment; filename="job_post_report.pdf"'

    # Write the PDF to the response.
    response.write(buffer.read())

    return response

@login_required
@user_passes_test(is_admin, login_url='/unauthorized_access/')
def generate_activity_log_report_view(request):
    activity_logs = Activity_Logs.objects.all()
    buffer = BytesIO()

    # Create the PDF object, using the BytesIO object as its "file."
    pdf = SimpleDocTemplate(buffer, pagesize=letter)

    # Create a list to hold all elements in the PDF
    elements = []

    # Add a title to the PDF
    elements.append(Paragraph("Activity Log Report", getSampleStyleSheet()['Title']))

    report_status = "This report provides information about user activities."
    elements.append(Paragraph(report_status, getSampleStyleSheet()['BodyText']))

    # Define the table data
    data = [['ID', 'Username', 'Activity', 'Timestamp']]

    # Add data rows
    for i, log in enumerate(activity_logs):
        data.append([
            i + 1,
            log.user.username,
            log.activity,
            log.timestamp.strftime("%Y-%m-%d %H:%M:%S"),  # Format the timestamp as needed
        ])

    # Customize the font size for the table
    table_style = TableStyle([
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),  # Adjust the font name as needed
        ('FONTSIZE', (0, 0), (-1, -1), 10),  # Adjust the font size as needed
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ])

    # Create the table with the customized style
    table = Table(data, colWidths=[30, 150, 250, 120])
    table.setStyle(table_style)

    # Add the table to the elements list
    elements.append(table)

    # Build the PDF
    pdf.build(elements)

    # File is now complete.
    buffer.seek(0)

    # Create a response object.
    response = HttpResponse(content_type="application/pdf")
    response["Content-Disposition"] = 'filename="activity_log_report.pdf"'

    # Write the PDF to the response.
    response.write(buffer.read())

    return response

@login_required
@user_passes_test(is_admin, login_url='/unauthorized_access/')
def generate_activity_log_report(request):
    activity_logs = Activity_Logs.objects.all()
    buffer = BytesIO()

    # Create the PDF object, using the BytesIO object as its "file."
    pdf = SimpleDocTemplate(buffer, pagesize=letter)

    # Create a list to hold all elements in the PDF
    elements = []

    # Add a title to the PDF
    elements.append(Paragraph("Activity Log Report", getSampleStyleSheet()['Title']))

    report_status = "This report provides information about user activities."
    elements.append(Paragraph(report_status, getSampleStyleSheet()['BodyText']))

    # Define the table data
    data = [['ID', 'Username', 'Activity', 'Timestamp']]

    # Add data rows
    for i, log in enumerate(activity_logs):
        data.append([
            i + 1,
            log.user.username,
            log.activity,
            log.timestamp.strftime("%Y-%m-%d %H:%M:%S"),  # Format the timestamp as needed
        ])

    # Customize the font size for the table
    table_style = TableStyle([
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),  # Adjust the font name as needed
        ('FONTSIZE', (0, 0), (-1, -1), 10),  # Adjust the font size as needed
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ])

    # Create the table with the customized style
    table = Table(data, colWidths=[30, 150, 250, 120])
    table.setStyle(table_style)

    # Add the table to the elements list
    elements.append(table)

    # Build the PDF
    pdf.build(elements)

    # File is now complete.
    buffer.seek(0)

    # Create a response object.
    response = HttpResponse(content_type="application/pdf")
    response["Content-Disposition"] = 'attachment; filename="activity_log_report.pdf"'

    # Write the PDF to the response.
    response.write(buffer.read())

    return response

@login_required
@user_passes_test(is_admin, login_url='/unauthorized_access/')
def adminlistActivity(request):
    activity_logs = Activity_Logs.objects.all()
    return render(request, "main/Admin/admin-list-activity.html", {'activity_logs': activity_logs})

def signupPopup(request):
    return render(request,"main/Signup-second.html")

def log_activity(request, action):
    user = request.user if request.user.is_authenticated else None
    if user:
        activity_log = Activity_Logs(user=user, activity=action, timestamp=datetime.now())
        activity_log.save()

def unauthorized_access(request):
    return render(request,"main/alert-page.html")