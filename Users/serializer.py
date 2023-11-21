from rest_framework import serializers
from .models import *


class Phone_Reg_srl(serializers.ModelSerializer):
    class Meta:
        model = Users
        fields = ("phone", )


class Otp_Reg_srl(serializers.ModelSerializer):
    class Meta:
        model = Users
        fields = ("phone", "otp")


class User_Srl(serializers.ModelSerializer):
    class Meta:
        model = Users
        fields = ('phone', 'otp', "name", 'surname', 'password')


class Log_user(serializers.ModelSerializer):
    class Meta:
        model = Users
        fields = ("phone", "password")
