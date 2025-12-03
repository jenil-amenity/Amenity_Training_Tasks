from django.contrib import admin
from django.urls import path, include
import auth.urls as urls

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('urls'))
]

