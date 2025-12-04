import re, random
from django.utils import timezone
from django.contrib.auth import authenticate
from rest_framework import serializers
from .models import CustomUser as User
from django.conf import settings
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth import get_user_model

User = get_user_model()

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)
    
    class Meta: 
        model = User
        fields = ['username', 'password', 'password2','email', 'first_name', 'last_name', 'phone', 'profile_pic']
    
    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError({"email":"Email id already exists"})
        return value
    
    def validate_password(self, value):
        pattern = r'^(?=.*[0-9])(?=.*[a-z])(?=.*[\W_]).{8,16}$'
        if not re.match(pattern, value):
            raise serializers.ValidateErrors("Password must be 8-16 characters long, include at least one lowercase letter, one digit, and one special character.")
        return value
            
    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({'password':"Password Field didn't match"})
        return attrs
    
    def create(self, validated_data):
        validated_data.pop('password2')
        otp = str(random.randint(100000, 999999))
            
        user = User.objects.create_user(
            **validated_data,
            otp=otp,
            otp_created=timezone.now(),
            is_active=False
        )
        user.save()
        return user    
    
class EditProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'phone', 'profile_pic']
        
    def validate_email(self, value):
        user = self.context['request'].user
        if User.objects.exclude(id = user.id).filter(email= value).exists():
            raise serializers.ValidationError({"email":"Email id already exists"})
        return value
    
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name']
        
class EmailLoginSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(write_only=True, required=True)