from django.urls import path, include
from .views import RegisterView, DeleteUserView
from rest_framework_simplejwt.views import TokenObtainPairView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', TokenObtainPairView.as_view(), name='login'), 
    path('delete_account/', DeleteUserView.as_view(), name='delete'),
    path('password_reset/', include('django_rest_passwordreset.urls', namespace='password_reset')),
]