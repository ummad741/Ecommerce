# django libraries
from django.shortcuts import render
from rest_framework_simplejwt.tokens import AccessToken, RefreshToken
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
from rest_framework import generics
# simple libraries

# local importing
from .models import *
from .serializer import *
from Users.models import Users

# Create your views here.


class Create_Admin(APIView):
    queryset = Admins.objects.all()
    serializer = Crete_Show_Srl()

    @swagger_auto_schema(request_body=Crete_Show_Srl)
    def post(self, request):
        serializer = Crete_Show_Srl(data=request.data)
        if serializer.is_valid():
            serializer.save()
        else:
            return Response(serializer.errors)


class All_Admins(APIView):
    queryset = Admins.objects.all()
    serializer = Crete_Show_Srl()

    def get(self, request):
        selected = Admins.objects.all()
        serializer = Crete_Show_Srl(selected, many=True)
        if serializer:
            return Response(serializer.data)
        else:
            return Response(serializer.errors)


class Delete_Admin(APIView):
    queryset = Admins.objects.all()
    # serializer = Forgot_pass()

    def delete(self, request, pk):
        user = Admins.objects.filter(id=pk)
        user.delete()
        return Response({"MSG": "Delete"})
