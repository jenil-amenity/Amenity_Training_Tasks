from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include
from .views import (RegisterView, ProfileView, LoginView,ResendOTPView, 
                    AllUsersView, EditProfileView, DeleteUserView, 
                    RequestPasswordResetView, PasswordResetConfirmView, VerifyOTPView)
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('verify_otp/', VerifyOTPView.as_view(), name='verify_otp'),
    path('resend_otp/', ResendOTPView.as_view(), name='resend_otp'),
    path('login/', LoginView.as_view(), name='login'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'), 
    path('edit_profile/', EditProfileView.as_view(), name='edit_profile'),
    path('getuser/', ProfileView.as_view(), name='getuser'),
    path('allusers/', AllUsersView.as_view(), name='all_users'),
    path('delete_account/', DeleteUserView.as_view(), name='delete'),
    path('password_reset/', RequestPasswordResetView.as_view(), name='password_reset'),
    path('password_reset_confirm/<uidb64>/<token>/', PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
]  

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) 