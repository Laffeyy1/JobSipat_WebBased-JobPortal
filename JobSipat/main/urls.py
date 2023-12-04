from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from . import views

urlpatterns = [
path("", views.index, name="index"),
path("signup/", views.signup, name="signup"),
path("home/", views.employeeHome, name="employeeHome"), 
path("profile/", views.employeeProfile, name="employeeProfile"), 
path("notif/", views.employeeNotif, name="employeeNotif"), 
path("edit/", views.employeeEdit, name="employeeEdit"), 
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)