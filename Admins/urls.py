from django.urls import path
from .views import *

urlpatterns = [
    path('Admin_Create/', Create_Admin.as_view()),
    path('All_admins', All_Admins.as_view()),
]
