from rest_framework import serializers
from .models import *


class Crete_Show_Srl(serializers.ModelSerializer):
    class Meta:
        model = Admins
        fields = '__all__'


class Login_SRL(serializers.ModelSerializer):
    class Meta:
        model = Admins
        fields = ('phone', 'password')


class All_products(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'
