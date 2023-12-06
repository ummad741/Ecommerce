# django libraries
from django.shortcuts import render
from rest_framework_simplejwt.tokens import AccessToken, RefreshToken
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
from rest_framework import generics
from rest_framework.parsers import MultiPartParser
from django.contrib.auth import logout
# local importing
from .models import *
from .serializer import *
from Users.models import Users

# Create your views here.

#! NAMING


class Create_Admin(APIView):
    queryset = Admins.objects.all()
    serializer = Crete_Show_Srl
    parser_classes = [MultiPartParser,]

    @swagger_auto_schema(request_body=Crete_Show_Srl)
    def post(self, request):
        serializer = Crete_Show_Srl(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors)


class All_Admins(APIView):
    queryset = Admins.objects.all()
    serializer = Crete_Show_Srl

    def get(self, request):
        selected = Admins.objects.all()
        serializer = Crete_Show_Srl(selected, many=True)
        if serializer:
            return Response(serializer.data)
        else:
            return Response(serializer.errors)


class Select_Admins(APIView):
    queryset = Users.objects.all()
    serializer = Crete_Show_Srl

    def get(self, request, pk):
        try:
            selected = Admins.objects.filter(id=pk).first()
        except:
            return Response({"MSg": "Bad request"}, status=400)
        serializer = Crete_Show_Srl(selected)
        if serializer:
            return Response(serializer.data)
        else:
            return Response(serializer.errors)


class Delete_Admin(APIView):
    queryset = Admins.objects.all()
    # serializer = Forgot_pass

    def delete(self, request, pk):
        user = Admins.objects.filter(id=pk)
        user.delete()
        return Response({"MSG": "Deleted"})


class Login(APIView):
    queryset = Admins.objects.all()
    serializer = Login_SRL
    parser_classes = [MultiPartParser,]

    @swagger_auto_schema(request_body=Login_SRL)
    def post(self, request):
        phone = request.data.get("phone")
        password = request.data.get("password")
        try:
            log_admins = Admins.objects.filter(
                phone=phone, password=password).first()
        except:
            return Response({"MSg": "Bad request"}, status=400)
        if log_admins:
            serializer = Login_SRL()
            access = AccessToken.for_user(log_admins)
            refresh = RefreshToken.for_user(log_admins)
            return Response({
                "access": str(access),
                "refresh": str(refresh),
                "serializer": serializer.data
            })
        else:
            return Response({"MSG": "ERROR"}, status=400)


class Logout_admins(APIView):
    queryset = Admins.objects.all()

    def get(self, request, pk):
        admin = Admins.objects.filter(id=pk).first()
        if admin:
            logout(request)
            return Response({"MSG": "Succsess"})
        else:
            return Response({"MSG": "error"})


class Products_check_and_save_views(APIView):
    queryset = Admins.objects.all()
    serialzer = All_products
    parser_classes = [MultiPartParser,]

    @swagger_auto_schema(request_body=All_products)
    def post(self, request, pk):
        try:
            admin = Admins.objects.filter(id=pk).first()
        except:
            return Response({"MSG": "Bad request"}, status=400)

        if admin.admins == 'admin':
            serializer = All_products(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            else:
                return Response(serializer.errors)
        else:
            return Response({"MSG": "you are not an admin"}, status=400)


class Super_admin_button(APIView):
    queryset = Admins.objects.all()

    def get(self, request, pk):
        try:
            superadmin = Admins.objects.filter(id=pk).first()
        except:
            return Response({"MSg": "There is no such admin"}, status=400)
        admin_info = []
        if superadmin.admins == 'Superadmin':
            admins = Admins.objects.filter(admins='admin').all()
            for i in admins:
                product_count = Product.objects.all().filter(admin_id=i.id).count()
                admin_info.append(
                    {
                        "Id": i.id,
                        "Name": i.name,
                        'Product_count': product_count
                    })
            return Response({"admin": admin_info}, status=200)
        else:
            return Response({"MSG": "There is no such admin"}, status=404)


class Dashboard(APIView):
    queryset = Product.objects.all()
    serealizer = All_products

    def get(self, request):
        products = Product.objects.all()
        serializer = All_products(products, many=True)
        if products:
            return Response(serializer.data)
        else:
            return Response({"MSG": "There is no such product"})


# class Create_Products(APIView):
#     queryset = Product.objects.all()
#     serializer = All_products
#     parser_classes = [MultiPartParser,]

#     @swagger_auto_schema(request_body=All_products)
#     def post(self, request):
#         serializer = All_products(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         else:
#             return Response(serializer.errors)
