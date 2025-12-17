from django.contrib.auth import get_user_model
from rest_framework import serializers

from apps.users.models import CustomerProfile


User = get_user_model()


class CustomerProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomerProfile
        fields = ["full_name", "phone", "driver_license_no", "address"]


class UserSerializer(serializers.ModelSerializer):
    profile = CustomerProfileSerializer(read_only=True)

    class Meta:
        model = User
        fields = ["id", "username", "email", "role", "profile"]
        read_only_fields = ["id", "role"]


class RegisterSerializer(serializers.Serializer):
    username = serializers.CharField()
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True, min_length=8)
    full_name = serializers.CharField()
    phone = serializers.CharField()
    driver_license_no = serializers.CharField()
    address = serializers.CharField()

    def validate_username(self, value):
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError("Username already taken.")
        return value

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("Email already registered.")
        return value

    def create(self, validated_data):
        profile_fields = {
            "full_name": validated_data.pop("full_name"),
            "phone": validated_data.pop("phone"),
            "driver_license_no": validated_data.pop("driver_license_no"),
            "address": validated_data.pop("address"),
        }
        user = User.objects.create_user(
            role=User.Role.CUSTOMER,
            **validated_data,
        )
        CustomerProfile.objects.create(user=user, **profile_fields)
        return user


class MeSerializer(serializers.ModelSerializer):
    profile = CustomerProfileSerializer()

    class Meta:
        model = User
        fields = ["id", "username", "email", "role", "profile"]
        read_only_fields = ["id", "username", "role"]

    def update(self, instance, validated_data):
        profile_data = validated_data.pop("profile", {})
        instance.email = validated_data.get("email", instance.email)
        instance.save(update_fields=["email"])

        profile, _ = CustomerProfile.objects.get_or_create(user=instance)
        for field, value in profile_data.items():
            setattr(profile, field, value)
        profile.save()
        return instance
