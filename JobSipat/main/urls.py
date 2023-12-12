from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from . import views

urlpatterns = [
path("", views.index, name="index"),
path("login/", views.index, name="login"),
path("signup/", views.signup, name="signup"),
path("signup2/", views.signupPopup, name="signup2"),
path("applicantHome/", views.employeeHome, name="applicantHome"), 
path("applicantViewJob/", views.applicantViewJob, name="applicantViewJob"), 
path('applicant-view-job/<int:job_post_id>/', views.applicantViewJob, name='applicantViewJob'),
path("applicantProfile/", views.employeeProfile, name="applicantProfile"), 
path("applicantNotif/", views.employeeNotif, name="applicantNotif"), 
path("applicantEdit/", views.employeeEdit, name="applicantEdit"),
path("logout/", views.logout_view, name="logout"),
path("listuser/", views.adminListUser, name="adminListUser"),
path("listactivity/", views.adminListActivity, name="adminListActivity"),
path("alertpage/", views.alertPage, name="alertPage"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)