from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.contrib.auth.views import PasswordResetConfirmView
from django.urls import reverse
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.core.mail import send_mail
from django.conf import settings
from rest_framework import status
from rest_framework.permissions import AllowAny,IsAuthenticated,IsAdminUser
from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import RegisterSerializer, UserSerializer, EditProfileSerializer, EmailLoginSerializer

# Get the custom user model
User = get_user_model()

# View for user registration
class RegisterView(generics.CreateAPIView):
    serializer_class = RegisterSerializer 
    permission_classes = [AllowAny]
    
    def perform_create(self, serializer):
        user = serializer.save()
        subject = "Verify your account"
        message = F"Your OTP code is: {user.otp}"
        
        send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [user.email], fail_silently=False)
        
        return user
    
    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        return Response({"detail": "Account Created Please Check your email for OTP to verifiy you account"}, status=status.HTTP_201_CREATED)
    
# View for OTP verification
class VerifyOTPView(APIView):
    permission_classes = [AllowAny]
    
    # Handle POST request for OTP verification
    def post(self, request):
        email = request.data.get('email')
        otp = request.data.get('otp')
        
        #
        if not email or not otp:
            return Response({"error":"Email and OTP are requires"}, status=status.HTTP_404_NOT_FOUND)

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response({"Error":"invalid email"}, status=404)
        
        if user.otp != otp:
            return Response({"error":"Invalid OTP"}, status=status.HTTP_400_BAD_REQUEST)
        
        user.is_verified = True
        user.is_active = True
        user.otp = None
        user.otp_created = None
        user.save()
        
        return Response({"detail":"Account verified successfully!"}, status=status.HTTP_200_OK)
    
class LoginView(APIView):
    permission_classes = [AllowAny]
    authentication_classes = []

    def post(self, request, *args, **kwargs):
        serializer = EmailLoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data['email']
        password = serializer.validated_data['password']

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response({"error": "Invalid email or password"}, status=status.HTTP_401_UNAUTHORIZED)

        if not user.check_password(password):
            return Response({"error": "Invalid email or password"}, status=status.HTTP_401_UNAUTHORIZED)

        if not user.is_verified:
            return Response({"error": "Please verify your email first"}, status=status.HTTP_403_FORBIDDEN)

        if not user.is_active:
            return Response({"error": "Account is inactive"}, status=status.HTTP_403_FORBIDDEN)

        refresh = RefreshToken.for_user(user)
        access = refresh.access_token

        return Response({
            "refresh": str(refresh),
            "access": str(access),
            "user_id": user.id,
            "email": user.email,
            "first_name": user.first_name,
            "last_name": user.last_name
        }, status=status.HTTP_200_OK)
    
class MeView(generics.RetrieveAPIView):
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_object(self):
        return self.request.user

class EditProfileView(generics.UpdateAPIView):
    serializer_class = EditProfileSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_object(self):
        return self.request.user
    
    
class DeleteUserView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    
    def delete(self, request, formate=None):
        user = request.user
        user.delete()
        
        return Response({"detail":"User deleted successfully!"}, status=status.HTTP_204_NO_CONTENT)

class RequestPasswordResetView(APIView):
    permission_classes = [AllowAny]
    
    def post(self, request):
        email = request.data.get('email')
        
        if not email:
            return Response({"error": "Email is required"}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response({"error": "User with this email does not exist"}, status=status.HTTP_404_NOT_FOUND)
        
        token_generator = PasswordResetTokenGenerator()
        token = token_generator.make_token(user)
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        
        reset_path = reverse('password_reset_confirm', kwargs={'uidb64': uid, 'token': token})
        reset_url = request.build_absolute_uri(reset_path)
        
        subject = "Password Reset Request"
        message = f"Click the link below to reset your password:\n{reset_url}"
        
        send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [user.email], fail_silently=False)
        
        return Response({"detail": "If an account with that email exists, an email was sent"}, status=status.HTTP_200_OK) 

class PasswordResetConfirmView(APIView):
    permission_classes = [AllowAny]
    
    def post(self, request, uidb64, token):
        password = request.data.get('password')
        password2 = request.data.get('password2')
        
        if not password or not password2:    
            return Response({"error": "Password and Password2 is required"}, status=status.HTTP_400_BAD_REQUEST)
        
        if password != password2:
            return Response({"error": "Passwords do not match"}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except Exception:
            return Response({"error": "Invalid Link"}, status=status.HTTP_400_BAD_REQUEST)
        
        token_generator = PasswordResetTokenGenerator()
        if not token_generator.check_token(user, token):
            return Response({"error": "Invalid or Expired Token"}, status=status.HTTP_400_BAD_REQUEST)
        
        user.set_password(password)
        user.save()
        
        return Response({"detail": "Password has been reset successfully"}, status=status.HTTP_200_OK)
    
class LogoutView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    
    def post(self, request):
        request.user.auth_token.delete()
        return Response({"detail":"Logged out successfully!"}, status=status.HTTP_200_OK)
            

