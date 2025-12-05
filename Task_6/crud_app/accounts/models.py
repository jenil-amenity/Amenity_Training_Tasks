from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import RegexValidator, EmailValidator 
import uuid
from django.utils import timezone

class CustomUser(AbstractUser):
    # customized user model
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    username = models.CharField(max_length=150, blank=True, null=True)
    email = models.EmailField(unique=True)
    
    phone_regex = RegexValidator(
        regex= r'^\d{1,3}\d{7,14}$',
        message= 'Phone number is not valid!'
    )
    phone = models.CharField(max_length=32, unique=True, null=True, blank=True, validators=[phone_regex])
    
    profile_pic = models.ImageField(upload_to='profiles/', blank=True, null=True)
    otp = models.CharField(max_length=6, blank=True, null=True)
    otp_created = models.DateTimeField(blank=True, null=True)
    is_verified = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']
    
    # methods for OTP and verification
    def mark_otp(self, code):
        self.otp = code
        self.otp_created = timezone.now()
        self.save(updated_fields=['otp', 'otp_created'])
    
    # method to verify user
    def verify_user(self):
        self.is_verified = True
        self.otp = None
        self.otp_created = None
        self.save(updated_fields=['is_verified', 'otp', 'otp_created'])
        
    # string representation
    def __str__(self):
        return self.email
    
    