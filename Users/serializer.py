from rest_framework import serializers
from django.contrib.auth.hashers import check_password, make_password
from .models import *
from Admins.models import *


class Phone_Reg_srl(serializers.ModelSerializer):
    class Meta:
        model = Users
        fields = ("phone", )


class Forgot_pass(serializers.ModelSerializer):
    class Meta:
        model = Users
        fields = ("phone", "otp", "password")


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


# class Change_Srl(serializers.Serializer):
#     old_password = serializers.CharField(write_only=True)
#     new_password = serializers.CharField(write_only=True)
#     confirm_password = serializers.CharField(write_only=True)

#     def validate(self, attrs):
#         new_password = attrs.get('new_password')
#         confirm_password = attrs.get('confirm_password')

#         if new_password != confirm_password:
#             raise serializers.ValidationError(
#                 {"MSG": "Passwords do not match"})

#         return attrs

#     def update(self, instance, validated_data):
#         old_password = validated_data.get('old_password')
#         checker = check_password(old_password, instance.password)
#         print(checker)
#         if checker:
#             raise serializers.ValidationError(
#                 {"MSG": "Sucsessfuly changed password"})

#         new_password = validated_data.get('new_password')
#         instance.password = make_password(new_password)
#         instance.save()
#         return instance

class Change_Srl(serializers.Serializer):
    old_password = serializers.CharField(write_only=True)
    new_password = serializers.CharField(write_only=True)
    confirm_password = serializers.CharField(write_only=True)


class Show_Users_Srl(serializers.ModelSerializer):
    class Meta:
        model = Users
        fields = "__all__"


class OrdersSrl(serializers.ModelSerializer):
    class Meta:
        model = Orders
        fields = "__all__"


class AllProductsSRL(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'


class Change_SRL(serializers.ModelSerializer):
    change_phone = serializers.CharField()

    class Meta:
        model = Users
        fields = ('change_phone',)


class DeleteOrderSrl(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ('title',)


class CardUserSrl(serializers.ModelSerializer):
    class Meta:
        model = Users
        fields = (
            'idp', 'seria', 'raqam', 'pasport',
            'image', 'card', 'card_number', 'addres', 'viloyat'
        )
