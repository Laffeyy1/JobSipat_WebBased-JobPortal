from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from . import views

urlpatterns = [
path("", views.index, name="index"),
path("login/", views.index, name="login"),
path("signup/", views.signup, name="signup"),
path("home/", views.employeeHome, name="employeeHome"), 
path("profile/", views.employeeProfile, name="employeeProfile"), 
path("notif/", views.employeeNotif, name="employeeNotif"), 
path("edit/", views.employeeEdit, name="employeeEdit"),
path("logout/", views.logout_view, name="logout"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)