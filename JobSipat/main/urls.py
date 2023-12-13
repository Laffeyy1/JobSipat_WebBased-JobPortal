from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from .views import applicantViewJob

from . import views

urlpatterns = [
path("", views.index, name="index"),
path("login/", views.index, name="login"),
path("signup/", views.signup, name="signup"),
path("signup2/", views.signupPopup, name="signup2"),
path("logout/", views.logout_view, name="logout"),
path("applicantHome/", views.applicantHome, name="applicantHome"), 
path("applicantViewJob/", views.applicantViewJob, name="applicantViewJob"), 
path('applicant-view-job/<int:job_post_id>/', views.applicantViewJob, name='applicantViewJob'),
path("applicantProfile/", views.applicantProfile, name="applicantProfile"), 
path("applicantNotif/", views.applicantNotif, name="applicantNotif"), 
path("applicantEdit/", views.applicantEdit, name="applicantEdit"),
path("employerHome/", views.employerHome, name="employerHome"), 
path("employerPostAd/", views.employerPostAd, name="employerPostAd"), 
path("employer/post/edit/<int:job_post_id>/", views.employerPostEdit, name="employerPostEdit"),
path("employerProfile/", views.employerProfile, name="employerProfile"), 
path("employerEdit/", views.employerEdit, name="employerEdit"), 
path("adminHome/", views.adminHome, name="adminHome"), 
path('job_generate_pdf_report_view/', views.job_generate_pdf_report_view, name='job_generate_pdf_report_view'),
path('job_generate_pdf_report/', views.job_generate_pdf_report, name='job_generate_pdf_report'),
path("adminListUser/", views.adminListUser, name="adminListUser"), 
path('edit_user/<int:user_id>/', views.edit_user, name='edit_user'),
path('delete_user/<int:user_id>/', views.delete_user, name='delete_user'),
path('create_user/', views.create_user, name='create_user'),
path('generate_pdf_report/', views.user_generate_pdf_report, name='generate_pdf_report'),
path('generate_pdf_report_view/', views.user_generate_pdf_report_view, name='generate_pdf_report_view'),
path("adminlistActivity/", views.adminlistActivity, name="adminlistActivity"), 
path('generate_activity_log_report_view/', views.generate_activity_log_report_view, name='generate_activity_log_report_view'),
path('generate_activity_log_report/', views.generate_activity_log_report, name='generate_activity_log_report'),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)