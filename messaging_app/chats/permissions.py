# chats/permissions.py

from rest_framework import permissions
from rest_framework.exceptions import PermissionDenied
from .models import Conversation, Message

class IsParticipantOfConversation(permissions.BasePermission):
    """
    Custom permission to:
    ✅ Allow only authenticated users
    ✅ Allow only participants to view/send/update/delete messages
    """

    def has_permission(self, request, view):
        # ✅ Check that user is authenticated
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        # ✅ Check permissions for message or conversation objects
        if isinstance(obj, Message):
            conversation = obj.conversation
        elif isinstance(obj, Conversation):
            conversation = obj
        else:
            return False

        if request.method in ['PUT', 'PATCH', 'DELETE']:
            # ✅ Only participants should update or delete
            if request.user not in conversation.participants.all():
                raise PermissionDenied("You are not allowed to modify this conversation or message.")

        # ✅ Allow read or create if participant
        return request.user in conversation.participants.all()
