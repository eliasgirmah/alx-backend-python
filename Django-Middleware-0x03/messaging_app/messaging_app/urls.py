from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    # 🛠 Django Admin Panel
    path('admin/', admin.site.urls),

    # 🔐 JWT Authentication Endpoints
    path('api/auth/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),       # Obtain access & refresh tokens
    path('api/auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),       # Refresh access token

    # 📦 API Routes for Messaging App
    path('api/', include('chats.urls')),

    # 🧪 Optional: Login/Logout for DRF Browsable API (Session Auth)
    path('api-auth/', include('rest_framework.urls')),
]
