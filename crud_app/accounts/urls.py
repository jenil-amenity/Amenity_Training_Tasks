from django.urls import path, include
from .views import (RegisterView, MeView, LoginView, UserListView, EditProfileView, DeleteUserView, RequestPasswordResetView, PasswordResetConfirmView, VerifyOTPView)
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('verify_otp/', VerifyOTPView.as_view(), name='verify_otp'),
    path('login/', LoginView.as_view(), name='login'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'), 
    path('edit_profile/', EditProfileView.as_view(), name='edit_profile'),
    path('me/', MeView.as_view(), name='me'),
    path("users/", UserListView.as_view(), name="user_list"),
    path('delete_account/', DeleteUserView.as_view(), name='delete'),
    path('password_reset/', RequestPasswordResetView.as_view(), name='password_reset'),
    path('password_reset_confirm/<uidb64>/<token>/', PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
]   