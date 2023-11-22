# django libraries
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
from rest_framework_simplejwt.tokens import AccessToken, RefreshToken
from rest_framework import generics
# simple libraries
import random
# local importing
from .models import *
from .serializer import *

# Create your views here.
otp_generation = random.randint(1111, 9999)


class Register_view_step1(APIView):
    queryset = Users.objects.all()
    serializer = Phone_Reg_srl()

    @swagger_auto_schema(request_body=Phone_Reg_srl)
    def post(self, request):

        request.data['otp'] = str(otp_generation)
        serializer = Otp_Reg_srl(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"MSG": "Successfully created", "OTP": otp_generation})
        else:
            return Response(serializer.errors)


class Register_step2(APIView):
    queryset = Users.objects.all()
    serializer = Otp_Reg_srl()

    @swagger_auto_schema(request_body=Otp_Reg_srl)
    def post(self, request):
        re_phone = request.data.get("phone")
        re_password = request.data.get("otp")
        check = Users.objects.filter(otp=re_password, phone=re_phone).first()
        if check:
            return Response({"MSG": "Succsesfuly"})
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)


class Main_Reg(APIView):
    queryset = Users.objects.all()
    serializer = User_Srl()

    @swagger_auto_schema(request_body=User_Srl)
    def post(self, request):
        phone = request.data.get("phone")
        name = request.data.get("name")
        surname = request.data.get("surname")
        password = request.data.get("password")

        user = Users.objects.get(phone=phone)
        if user:
            user.name = name
            user.surname = surname
            user.password = password
            user.save()

            access = AccessToken.for_user(user)
            refresh = RefreshToken.for_user(user)

            return Response({
                "access": str(access),
                "refresh": str(refresh),
                "data": User_Srl(user).data
            })
        else:
            return Response({"MSG": "ERROR"}, status=status.HTTP_400_BAD_REQUEST)

        # user = Users.objects.filter(phone=phone).update(
        #     name=name, surname=surname, password=password)
        # print(user)
        # if user:
        #     access = AccessToken.for_user(user)
        #     refresh = RefreshToken.for_user(user)
        #     return Response({
        #         "access": access,
        #         "refresh": refresh,
        #         "data": user
        #     })
        # else:
        #     return Response({"MSG": "ERROR"}, status=status.HTTP_400_BAD_REQUEST)


class Login(APIView):
    queryset = Users.objects.all()
    serializer = Log_user()

    @swagger_auto_schema(request_body=Log_user)
    def post(self, request):
        phone = request.data.get("phone")
        password = request.data.get("password")
        log_user = Users.objects.filter(phone=phone, password=password).first()
        print(log_user)
        if log_user:
            access = AccessToken.for_user(log_user)
            refresh = RefreshToken.for_user(log_user)
            serializer = Log_user(log_user)
            return Response({
                "access": str(access),
                "refresh": str(refresh),
                "serializer": serializer.data
            })
        else:
            return Response({"MSG": "ERROR"}, status=status.HTTP_400_BAD_REQUEST)


class Change_Password(generics.UpdateAPIView):
    queryset = Users.objects.all()
    serializer_class = Change_Srl()
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(request_body=Change_Srl)
    def put(self, request,pk):
        serializer = Change_Srl(instance=self.request.user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"MSG": "Change your password succsess"})
        else:
            return Response(serializer.errors)


class All_Users(APIView):
    queryset = Users.objects.all()
    serializer = Show_Users_Srl()

    def get(self, request):
        selected = Users.objects.all()
        serializer = Show_Users_Srl(selected, many=True)
        if serializer:
            return Response(serializer.data)
        else:
            return Response(serializer.errors)


class Forgot_Password_step1(APIView):
    queryset = Users.objects.all()
    serializer = Phone_Reg_srl()

    @swagger_auto_schema(request_body=Phone_Reg_srl)
    def post(self, request):
        phone = request.data.get("phone")
        user = Users.objects.filter(phone=phone).first()
        if user:
            return Response({"OTP": user.otp})
        else:
            return Response({"MSG": "Bunday User yoq"})


class Forgot_Password_step2(APIView):
    queryset = Users.objects.all()
    serializer = Forgot_pass()

    @swagger_auto_schema(request_body=Forgot_pass)
    def post(self, request):
        phone = request.data.get("phone")
        otp = request.data.get("otp")
        password = request.data.get("password")
        try:
            user = Users.objects.all().filter(phone=phone, otp=otp).update(password=password)
            return Response({"MSG": "Malades gozal"})
        except:
            return Response({"MSG": "qalesan"})
