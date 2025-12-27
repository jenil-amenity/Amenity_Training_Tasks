from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.contrib.auth.views import PasswordResetConfirmView
from django.urls import reverse
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.core.mail import send_mail
from django.conf import settings
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
<<<<<<< Updated upstream:crud_app/accounts/views.py
from .serializers import RegisterSerializer, UserSerializer, EditProfileSerializer, EmailLoginSerializer, AllUsersSerializer
=======
from utils.responses import APIResponse
from .serializers import (
    RegisterSerializer,
    UserSerializer,
    EditProfileSerializer,
    EmailLoginSerializer,
    AllUserSerializer,
    ChangePasswordSerializer,
)
>>>>>>> Stashed changes:Task_6/crud_app/accounts/views.py

# Get the custom user model
User = get_user_model()


# View for user registration
class RegisterView(generics.CreateAPIView):
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]
    authentication_classes = []  # avoid JWT auth on register

    # Override perform_create to send OTP email
    def perform_create(self, serializer):
        user = serializer.save()
        subject = "Verify your account"
        message = f"Your OTP code is: {user.otp}"

        # Send OTP email to user
        send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,
            [user.email],
            fail_silently=False,
        )

        return user

    # Override create to customize response
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        if not serializer.is_valid():
            return APIResponse.get_serializer_error_response(
                return_code=APIResponse.Codes.VALIDATION_ERROR,
                serializer_errors=serializer.errors,
            )

        self.perform_create(serializer)

        print(request.data)

        return APIResponse.get_success_response(
            return_code=APIResponse.Codes.REGISTRATION_SUCCESS,
            data=serializer.data,
            status_code=status.HTTP_201_CREATED,
        )


# View for OTP verification
class VerifyOTPView(APIView):
    permission_classes = [AllowAny]
    authentication_classes = []  # avoid JWT auth on verify

    # Handle POST request for OTP verification
    def post(self, request):
        email = request.data.get("email")
        otp = request.data.get("otp")

        # Validate input
        if not email or not otp:
            return APIResponse.get_error_response(
                return_code=APIResponse.Codes.EMAIL_OTP_REQUIRED
            )

        # Fetch user and verify OTP
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return APIResponse.get_error_response(
                return_code=APIResponse.Codes.USER_NOT_FOUND
            )

        # Check if OTP matches
        if user.otp != otp:
            return APIResponse.get_error_response(
                return_code=APIResponse.Codes.OTP_VERIFICATION_FAILED,
                message="OTP is invalid.",
            )

        # Check if OTP is expired
        if user.is_otp_expired():
            return APIResponse.get_error_response(
                return_code=APIResponse.Codes.OTP_EXPIRED, message="OTP expired."
            )

        # Mark user as verified
        user.is_verified = True
        user.is_active = True
        user.otp = None
        user.otp_created = None
        user.save()

        return APIResponse.get_success_response(
            return_code=APIResponse.Codes.OTP_VERIFIED
        )


# View for Resent OTP
class ResendOTPView(APIView):
    permission_classes = [AllowAny]
    authentication_classes = []  # avoid JWT auth on resend otp

    # Handle POST request to resend OTP
    def post(self, request):
        email = request.data.get("email")

        # Validate input
        if not email:
            return APIResponse.get_error_response(
                return_code=APIResponse.Codes.EMAIL_REQUIRED
            )

        # Fetch user by email
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return APIResponse.get_error_response(
                return_code=APIResponse.Codes.USER_NOT_FOUND
            )

        # Generate new OTP
        user.mark_otp()

        # Send OTP email
        subject = "Resend OTP Code"
        message = f"Your new OTP code is: {user.otp}"
        user.save()
        send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,
            [user.email],
            fail_silently=False,
        )

        return APIResponse.get_success_response(
            return_code=APIResponse.Codes.OTP_RESENT
        )


# View for user login
class LoginView(APIView):
    permission_classes = [AllowAny]
    authentication_classes = []

    # Handle POST request for login
    def post(self, request, *args, **kwargs):
        serializer = EmailLoginSerializer(data=request.data)

        if not serializer.is_valid():
            return APIResponse.get_serializer_error_response(
                return_code=APIResponse.Codes.VALIDATION_ERROR,
                serializer_errors=serializer.errors,
            )

        # # Extract email and password
        email = serializer.validated_data["email"]
        password = serializer.validated_data["password"]

        user = User.objects.filter(email=email).first()

        # Authenticate user
        if not user or not user.check_password(password):
            return APIResponse.get_error_response(
                return_code=APIResponse.Codes.LOGIN_CREDENTIAL_INVALID,
                message="Invalid Email or Password",
            )

        # Check if User is verified and active
        if not user.is_verified:
            return APIResponse.get_error_response(
                return_code=APIResponse.Codes.ACCOUNT_NOT_VERIFIED,
                message="Account is not verified",
            )

        # Check if User is active
        if not user.is_active:
            return APIResponse.get_error_response(
                return_code=APIResponse.Codes.ACCOUNT_INACTIVE,
                message="Your account is not active",
            )

        # Generate JWT tokens
        refresh = RefreshToken.for_user(user)
        access = refresh.access_token

        # Formate Data
        data = {
            "tokens": {"refresh": str(refresh), "access": str(access)},
            "user": {
                "user_id": str(user.id),
                "username": user.username,
                "email": user.email,
                "first_name": user.first_name,
                "last_name": user.last_name,
                "profile_pic": str(user.profile_pic.url) if user.profile_pic else None,
                # "profile_pic": profile_pic_url,
            },
        }

        return APIResponse.get_success_response(
            return_code=APIResponse.Codes.LOGIN_SUCCESS, data=data
        )


# View to get current user details
class ProfileView(generics.RetrieveAPIView):
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    # Get the current user object
    def get_object(self):
        return self.request.user
    
class UserListView(APIView):
    permission_classes = [permissions.IsAuthenticated]  

<<<<<<< Updated upstream:crud_app/accounts/views.py
    def get(self, request):
        users = User.objects.all()
        serializer = AllUsersSerializer(users, many=True)
        return Response(serializer.data)
    
=======
    # Override retrieve to customize response
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return APIResponse.get_success_response(
            return_code=APIResponse.Codes.PROFILE_RETRIEVED, data=serializer.data
        )


# View to list all users (admin only)
class AllUsersView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    # Handle GET request to list all users
    def get(self, request):
        users = User.objects.all()
        serializer = AllUserSerializer(users, many=True)
        return APIResponse.get_success_response(
            return_code=APIResponse.Codes.USERS_LIST_RETRIEVED, data=serializer.data
        )


>>>>>>> Stashed changes:Task_6/crud_app/accounts/views.py
# View to edit user profile
class EditProfileView(generics.UpdateAPIView):
    serializer_class = EditProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    # Get the current user object
    def get_object(self):
        return self.request.user

    # Override update to customize response
    def update(self, request, *args, **kwargs):
        try:
            partial = kwargs.pop("partial", False)
            instance = self.get_object()
            serializer = self.get_serializer(
                instance, data=request.data, partial=partial
            )

            if not serializer.is_valid():
                return APIResponse.get_serializer_error_response(
                    return_code=APIResponse.Codes.VALIDATION_ERROR,
                    serializer_errors=serializer.errors,
                )

            self.perform_update(serializer)

            return APIResponse.get_success_response(
                return_code=APIResponse.Codes.PROFILE_UPDATED, data=serializer.data
            )
        except:
            import traceback

            traceback.print_exc()

            return APIResponse.get_success_response(
                return_code=APIResponse.Codes.PROFILE_UPDATED, data={}
            )


# View to delete user account
class DeleteUserView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    # Handle DELETE request to delete user account
    def delete(self, request, formate=None):
        user = request.user
        user.delete()

        return APIResponse.get_success_response(
            return_code=APIResponse.Codes.USER_DELETED_SUCCESS
        )


# View to request password reset
class RequestPasswordResetView(APIView):
    permission_classes = [AllowAny]
    authentication_classes = []  # avoid JWT auth on password reset request

    # Handle POST request to send password reset email
    def post(self, request):
        email = request.data.get("email")

        # Validate input
        if not email:
            return APIResponse.get_error_response(
                return_code=APIResponse.Codes.EMAIL_REQUIRED,
                message="Email ID is required!",
            )

        # Fetch user by email
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return APIResponse.get_error_response(
                return_code=APIResponse.Codes.EMAIL_NOT_FOUND,
                message="Email id with this user not found!",
            )

        # Generate Otp
        user.mark_otp()

        # Generate password reset token and URL
        token_generator = PasswordResetTokenGenerator()
        token = token_generator.make_token(user)
        uid = urlsafe_base64_encode(force_bytes(user.pk))

        # frontend url
        forontend_url = "https://subhumid-continuately-tiana.ngrok-free.dev"
        reset_url = f"{forontend_url}/password_reset_confirm/{uid}/"

        # Build password reset URL
        # reset_path = reverse('password_reset_confirm', kwargs={'uidb64': uid})
        # reset_url = request.build_absolute_uri(reset_path)
        print(reset_url)

        # Send password reset email
        subject = "Password Reset Request"
        message = (
            f"Use beloq otp to reset password:\n\n"
            f"OTP: {user.otp}\n\n"
            f"This OTP is valid for 5 minutes only.\n\n"
            f"Click the link below to reset your password:\n\n{reset_url}"
        )

        user.save()

        send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,
            [user.email],
            fail_silently=False,
        )

        return APIResponse.get_success_response(
            return_code=APIResponse.Codes.PASSWORD_RESET_EMAIL_SENT
        )


# View to confirm password reset
class PasswordResetConfirmView(APIView):
    permission_classes = [AllowAny]
    authentication_classes = []  # avoid JWT auth on password reset confirm

    # Handle POST request to reset password
    def post(self, request, uidb64):
        otp = request.data.get("otp")
        password = request.data.get("password")
        password2 = request.data.get("password2")

        # Decode uid and fetch user
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except Exception:
            return APIResponse.get_error_response(
                return_code=APIResponse.Codes.INVALID_LINK, message="Invalid link!"
            )

        # Validate OTP
        if not otp:
            return APIResponse.get_error_response(
                return_code=APIResponse.Codes.OTP_REQUIRED, message="OTP is required!"
            )

        if str(user.otp) != str(otp):
            return APIResponse.get_error_response(
                return_code=APIResponse.Codes.OTP_INVALID, message="Invalid OTP!"
            )

        if user.is_otp_expired():
            return APIResponse.get_error_response(
                return_code=APIResponse.Codes.OTP_EXPIRED, message="OTP is expired!"
            )

        # Validate input
        if not password or not password2:
            return APIResponse.get_error_response(
                return_code=APIResponse.Codes.PASSWORD_REQUIRED,
                message="Password Required!",
            )

        # Check if passwords match
        if password != password2:
            return APIResponse.get_error_response(
                return_code=APIResponse.Codes.PASSWORDS_DO_NOT_MATCH,
                message="Password is not matched!",
            )

        # Validate token
        # token_generator = PasswordResetTokenGenerator()
        # if not token_generator.check_token(user, token):
        #     return APIResponse.get_error_response(
        #         return_code=APIResponse.Codes.TOKEN_INVALID, message="Inavlid Token!"
        #     )

        user.set_password(password)
        user.otp = None
        user.otp_created = None
        user.save()

        return APIResponse.get_success_response(
            return_code=APIResponse.Codes.PASSWORD_CHANGE_SUCCESS
        )


# View for user logout
class LogoutView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    # Handle POST request to logout user
    def post(self, request):
        try:
            request.user.auth_token.delete()
        except:
            pass  # Token might not exist, continue anyway
        return APIResponse.get_success_response(
            return_code=APIResponse.Codes.LOGOUT_SUCCESS
        )


# Change Password View
class ChangePasswordView(generics.UpdateAPIView):
    serializer_class = ChangePasswordSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(
            data=request.data, context={"request": request}
        )

        if not serializer.is_valid():
            return APIResponse.get_serializer_error_response(
                return_code=APIResponse.Codes.VALIDATION_ERROR,
                serializer_errors=serializer.errors,
            )

        serializer.save()

        return APIResponse.get_success_response(
            return_code=APIResponse.Codes.PASSWORD_CHANGE_SUCCESS,
            data={"message": "Password updated successfully"},
        )
