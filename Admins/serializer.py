from rest_framework import serializers
from .models import *


class Crete_Show_Srl(serializers.ModelSerializer):

    class Meta:
        model = Admins
        fields = '__all__'
