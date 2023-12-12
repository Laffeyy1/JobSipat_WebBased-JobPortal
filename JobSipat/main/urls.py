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

path("listuser/", views.adminListUser, name="adminListUser"),
path("listactivity/", views.adminListActivity, name="adminListActivity"),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)