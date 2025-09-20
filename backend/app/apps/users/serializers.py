from __future__ import annotations

from django.contrib.auth import get_user_model
from rest_framework import serializers

from app.apps.users.models import Customer

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "email", "full_name", "role"]


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    phone = serializers.CharField(write_only=True)
    driver_license_no = serializers.CharField(write_only=True)
    address = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ["email", "password", "full_name", "role", "phone", "driver_license_no", "address"]
        extra_kwargs = {"role": {"required": False}}

    def create(self, validated_data):
        phone = validated_data.pop("phone")
        driver_license_no = validated_data.pop("driver_license_no")
        address = validated_data.pop("address")
        password = validated_data.pop("password")
        user = User.objects.create_user(password=password, **validated_data)
        if user.role == User.Role.CUSTOMER:
            Customer.objects.create(
                user=user,
                phone=phone,
                driver_license_no=driver_license_no,
                address=address,
            )
        return user
