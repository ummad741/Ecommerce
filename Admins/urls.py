from django.urls import path
from .views import *
# Naming
urlpatterns = [
    path('Create/Admins', Create_Admin.as_view()),
    path('Show/All_admins/', All_Admins.as_view()),
    path('Show/Selected_admins/<int:pk>/', Select_Admins.as_view()),
    path("Delete/Admin/", Delete_Admin.as_view()),
    path('Logout/Admins/<int:pk>/', Logout_admins.as_view()),
    path('Login/Admins/', Login.as_view()),
    path('Productcheck/Admins/<int:pk>/',
         Products_check_and_save_views.as_view()),
    path('Superadmin/jobs/<int:pk>/', Super_admin_button.as_view())
]
