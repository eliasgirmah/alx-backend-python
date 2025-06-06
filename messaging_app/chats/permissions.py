# messaging_app/chats/permissions.py

from rest_framework.permissions import BasePermission

class IsParticipantOfConversation(BasePermission):
    """
    Custom permission: only participants of a conversation can access it or its messages.
    """

    def has_object_permission(self, request, view, obj):
        # Check if this is a Message object (has a conversation)
        if hasattr(obj, 'conversation'):
            return request.user in obj.conversation.participants.all()

        # If it's a Conversation object
        if hasattr(obj, 'participants'):
            return request.user in obj.participants.all()

        return False
