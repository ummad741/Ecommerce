from django.urls import path
from .views import *

urlpatterns = [
    path("Users/phone_reg/", Register_view_step1.as_view()),
    path("Users/otp_reg/", Register_step2.as_view()),
    path("Users/Main_reg/", Main_Reg.as_view()),
    path("Users/Login/", Login.as_view()),
    path("Users/<int:pk>/Change_Password/", Change_Password.as_view()),
    path("Users/All_users/", All_Users.as_view()),
    path("Users/Select_User", Select_User.as_view()),
    path("Users/Forgot_step1/", Forgot_Password_step1.as_view()),
    path("Users/Forgot_step2/", Forgot_Password_step2.as_view()),
    path("Users/Delete_User/<int:pk>/", Delete_User.as_view()),
]
