from django.urls import path, include
from rest_framework_nested.routers import DefaultRouter, NestedDefaultRouter
from .views import ConversationViewSet, MessageViewSet
from .auth import MyTokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView

# 🔐 Custom Token View using your serializer
class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer

# 🔁 Main router for Conversations
router = DefaultRouter()
router.register(r'conversations', ConversationViewSet, basename='conversation')

# 📬 Nested router for Messages under Conversations
conversations_router = NestedDefaultRouter(router, r'conversations', lookup='conversation')
conversations_router.register(r'messages', MessageViewSet, basename='conversation-messages')

urlpatterns = [
    # JWT token endpoint using custom serializer
    path('token/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),

    # API endpoints for conversations and nested messages
    path('', include(router.urls)),
    path('', include(conversations_router.urls)),
]
