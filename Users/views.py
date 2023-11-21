# django libraries
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
from rest_framework_simplejwt.tokens import AccessToken, RefreshToken
# simple libraries
import random
# local importing
from .models import *
from .serializer import *


# Create your views here.


class Register_view_step1(APIView):
    queryset = Users.objects.all()
    serializer = Phone_Reg_srl

    @swagger_auto_schema(request_body=Phone_Reg_srl)
    def post(self, request):
        otp_generation = random.randint(1111, 9999)
        request.data['otp'] = str(otp_generation)
        serializer = Otp_Reg_srl(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"MSG": "Successfully created", "OTP": otp_generation})
        else:
            return Response(serializer.errors)


class Register_step2(APIView):
    queryset = Users.objects.all()
    serializer = Otp_Reg_srl

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
    serializer = User_Srl

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
    serializer = Log_user

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


class Forgot_Password(APIView):
    @swagger_auto_schema(request_body='srl')
    def post(self, request):
        pass

        #     access = AccessToken.for_user(user)
        #     refersh = RefreshToken.for_user(user)
        #     serialzier = User_Srl(user)
        #     if serialzier.is_valid():
        #         serialzier.save()
        #         return Response({
        #             "access": str(access),
        #             'refresh': str(refersh),
        #             'data': serialzier.data
        #         })
        #     else:
        #         return Response(serialzier.errors, status=status.HTTP_400_BAD_REQUEST)\
