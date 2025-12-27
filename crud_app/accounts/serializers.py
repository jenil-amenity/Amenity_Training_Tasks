import re, random
from django.utils import timezone
from django.contrib.auth import authenticate
from rest_framework import serializers
from .models import CustomUser as User
from django.conf import settings
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth import get_user_model
from utils.responses import APIResponse
from utils.base_serializer import BaseModelSerializer, BaseSerializerSerializer

User = get_user_model()


# Serializer for user registration
class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True)
    password2 = serializers.CharField(write_only=True, required=True)
    phone = serializers.CharField(required=False, allow_blank=True, allow_null=True)

    class Meta:
        model = User
        fields = [
            "username",
            "password",
            "password2",
            "email",
            "first_name",
            "last_name",
            "phone",
            "profile_pic",
        ]

    def validate_username(self, value):
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError(
                APIResponse.Codes._error_messages.get(APIResponse.Codes.USER_EXISTS)
            )
        return value

    # Custom validation for email and password
    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError(
                APIResponse.Codes._error_messages.get(
                    APIResponse.Codes.EMAIL_ALREADY_EXISTS,
                )
            )
        return value

    def validate_phone(self, value):
        if value in [None, ""]:
            return None

        value = value.strip()
        if value.isdigit():
            raise serializers.ValidationError(
                APIResponse.Codes._error_messages.get(
                    APIResponse.Codes.PHONE_ONLY_DIGIT,
                    "Phonenumber must contain only digit.",
                )
            )

        if User.objects.filter(phone=value).exists():
            raise serializers.ValidationError(
                APIResponse.Codes._error_messages.get(
                    APIResponse.Codes.PHONE_ALREADY_EXISTS,
                    "A user with this phone already exists.",
                )
            )
        return value

    # Custom password validation
    def validate_password(self, value):
        pattern = r"^(?=.*[0-9])(?=.*[a-z])(?=.*[\W_]).{8,16}$"
        if not re.match(pattern, value):
            raise serializers.ValidationError(
                APIResponse.Codes._error_messages.get(
                    APIResponse.Codes.PASSWORD_LENGTH_INVALID,
                )
            )
        return value

    # Cross-field validation for matching passwords
    def validate(self, attrs):
        if attrs["password"] != attrs["password2"]:
            raise serializers.ValidationError(
                {
                    "password2": APIResponse.Codes._error_messages.get(
                        APIResponse.Codes.PASSWORDS_DO_NOT_MATCH,
                        "Passwords do not match.",
                    )
                }
            )
        return attrs

    # Create method to create user instance
    def create(self, validated_data):
        validated_data.pop("password2")

        otp = str(random.randint(100000, 999999))

        user = User.objects.create_user(
            **validated_data,
            otp=otp,
            otp_created=timezone.now(),
            is_active=False,
        )
        user.save()
        return user


# Serializer for editing user profile
class EditProfileSerializer(serializers.ModelSerializer):
    phone = serializers.CharField(required=False, allow_blank=True, allow_null=True)

    class Meta:
        model = User
        fields = [
            "username",
            "first_name",
            "last_name",
            "phone",
            "profile_pic",
        ]

    # Custom validation for email uniqueness
    def validate_email(self, value):
        user = self.context["request"].user
        if User.objects.exclude(id=user.id).filter(email=value).exists():
            raise serializers.ValidationError(
                APIResponse.Codes._error_messages.get(
                    APIResponse.Codes.EMAIL_ALREADY_EXISTS, "Email already exists."
                )
            )
        return value

    def validate_phone(self, value):
        if value in [None, ""]:
            return None

        user = self.context["request"].user
        if User.objects.exclude(id=user.id).filter(phone=value).exists():
            raise serializers.ValidationError(
                APIResponse.Codes._error_messages.get(
                    APIResponse.Codes.PHONE_ALREADY_EXISTS,
                    "A user with this phone already exists.",
                )
            )
        return value


# Serializer for user details
class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
<<<<<<< Updated upstream:crud_app/accounts/serializers.py
        fields = ['id', 'username', 'email', 'first_name', 'last_name']

class AllUsersSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'id', 'username', 'email',
            'first_name', 'last_name',
            'phone','profile_pic', 'is_verified'
        ]

# Serializer for email login   
=======
        fields = [
            "id",
            "username",
            "email",
            "first_name",
            "last_name",
            "profile_pic",
            "phone",
        ]


# Serializer for all user details
class AllUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = [
            "id",
            "username",
            "email",
            "first_name",
            "last_name",
            "phone",
            "profile_pic",
            "is_verified",
        ]


# Serializer for email login
>>>>>>> Stashed changes:Task_6/crud_app/accounts/serializers.py
class EmailLoginSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(write_only=True, required=True)


# Serializer for Change password
class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(write_only=True, required=True)
    new_password = serializers.CharField(write_only=True, required=True)
    confirm_new_password = serializers.CharField(write_only=True, required=True)

    # Validate old password
    def validate_old_password(self, value):
        user = self.context["request"].user

        if not user.check_password(value):
            raise serializers.ValidationError(
                APIResponse.Codes._error_messages.get(
                    APIResponse.Codes.OLD_PASSWORD_INVALID, "Old password is incorrect."
                )
            )
        return value

    # Validate password format
    def validate_new_password(self, value):
        pattern = r"^(?=.*[0-9])(?=.*[a-zA-Z])(?=.*[\W_]).{8,16}$"

        if not re.match(pattern, value):
            raise serializers.ValidationError(
                APIResponse.Codes._error_messages.get(
                    APIResponse.Codes.PASSWORD_VALIDATION_FAILED,
                    "Password must be 8–16 chars, contain letters, numbers & special chars.",
                )
            )
        return value

    # Cross-field validation
    def validate(self, attrs):
        old_password = attrs.get("old_password")
        new_password = attrs.get("new_password")
        confirm_new_password = attrs.get("confirm_new_password")

        print(old_password, new_password)

        # New password cannot be same as old
        if old_password == new_password:
            raise serializers.ValidationError(
                APIResponse.Codes._error_messages.get(
                    APIResponse.Codes.SAME_PASSWORD,
                    "New password cannot be the same as old password.",
                )
            )

        # Confirm password must match
        if new_password != confirm_new_password:
            raise serializers.ValidationError(
                APIResponse.Codes._error_messages.get(
                    APIResponse.Codes.CONFIRM_PASSWORD_INVALID,
                    "Confirm password does not match.",
                )
            )

        return attrs

    # Save the new password
    def save(self):
        user = self.context["request"].user
        new_password = self.validated_data["new_password"]
        user.set_password(new_password)
        user.save()
        return user
