from rest_framework import serializers
from .models import *


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


class Change_Srl(serializers.ModelSerializer):
    old = serializers.CharField(write_only=True)
    new = serializers.CharField(write_only=True)
    second = serializers.CharField(write_only=True)

    class Meta:
        model = Users
        fields = ('old', 'new', 'second')

    # attrs bu dict
    def validate(self, attrs):

        if attrs['new'] != attrs['second']:
            raise serializers.ValidationError(
                {"MSG": "Passwords do not match"})
        return attrs

    def update(self, instance, validated_data):
        old_pass = validated_data.get("old")
        print(old_pass)
        if not instance.check_password(old_pass):
            print("kirmayapti")
            raise serializers.ValidationError(
                {"MSG": "Incorrect old password"})

        print("zor")
        new_pass = validated_data
        instance.set_password(new_pass)
        instance.save()
        print(instance)
        return instance


class Show_Users_Srl(serializers.ModelSerializer):
    class Meta:
        model = Users
        fields = "__all__"
