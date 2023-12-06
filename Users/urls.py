from django.urls import path
from .views import *
# Naming
urlpatterns = [
    path("Register/phone/", Register_view_step1.as_view()),
    path("Register/otp/", Register_step2.as_view()),
    path("Register/Main/", Main_Reg.as_view()),
    path('CardUser/<int:pk>/', CardUser.as_view()),
    path("Login/User", Login.as_view()),
    path("Lougout/User/<int:pk>/", Logout_users.as_view()),
    path("<int:pk>/ChangePassword/", Change_Password.as_view()),
    path('phone/Change/<int:pk>/', Phone_Changer.as_view()),
    path("Forgot/step1/", Forgot_Password_step1.as_view()),
    path("Forgot/step2/", Forgot_Password_step2.as_view()),
    path("Show/AllUsers/", All_Users.as_view()),
    path("Show/SelectUsers/", Select_User.as_view()),
    path("Delete/User/<int:pk>/", Delete_User.as_view()),
    # Orders
    path("Orders/Create/", OrderViews.as_view()),
    path('Orders/Calc/<int:pk>/', Calculate_cash_order.as_view()),
    path('Orders/show_Orders/<int:pk>/', Users_Order_all_views.as_view()),
]
