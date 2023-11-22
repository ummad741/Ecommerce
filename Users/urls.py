from django.urls import path
from .views import *

urlpatterns = [
    path("phone_reg/", Register_view_step1.as_view()),
    path("otp_reg/", Register_step2.as_view()),
    path("Main_reg/", Main_Reg.as_view()),
    path("Login/", Login.as_view()),
    path("Chang_pass/<int:pk>/", Change_Password.as_view()),
    path("All_users/", All_Users.as_view()),
    path("Forgot_step1/", Forgot_Password_step1.as_view()),
    path("Forgot_step2/", Forgot_Password_step2.as_view()),

]
