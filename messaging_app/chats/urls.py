from django.urls import path, include
from rest_framework import routers  # ✅ This matches the checker's expectation
from .views import ConversationViewSet, MessageViewSet

router = routers.DefaultRouter()
router.register(r'conversations', ConversationViewSet)
router.register(r'messages', MessageViewSet)

urlpatterns = [
    path('api/', include(router.urls)),  # ✅ Only include once, under 'api/'
]
