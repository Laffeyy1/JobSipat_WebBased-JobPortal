from django.urls import path

from . import views

urlpatterns = [
path("", views.index, name="index"),
path("signup/", views.signup, name="signup"),
path("home/", views.employeeHome, name="employeeHome"), 
path("profile/", views.employeeProfile, name="employeeProfile"), 
path("notif/", views.employeeNotif, name="employeeNotif"), 
path("edit/", views.employeeEdit, name="employeeEdit"), 
]