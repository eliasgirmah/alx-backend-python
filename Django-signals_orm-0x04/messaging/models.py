from django.db import models
from django.contrib.auth.models import User
from .managers import UnreadMessagesManager


class Message(models.Model):
    """
    Model representing a message sent from one user to another,
    supporting replies (threaded conversations), read status, and edit tracking.
    """
    sender = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='sent_messages'
    )
    receiver = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='received_messages'
    )
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    edited = models.BooleanField(default=False)
    parent_message = models.ForeignKey(
        'self', null=True, blank=True, on_delete=models.CASCADE, related_name='replies'
    )
    read = models.BooleanField(default=False)

    # Managers
    objects = models.Manager()  # Default manager
    unread = UnreadMessagesManager()  # Custom manager for unread messages

    def __str__(self):
        return f"From {self.sender} to {self.receiver} at {self.timestamp}"


class MessageHistory(models.Model):
    """
    Keeps a history of edits made to messages.
    Stores old content, who edited, and when.
    """
    message = models.ForeignKey(
        Message, on_delete=models.CASCADE, related_name='history'
    )
    old_content = models.TextField()
    edited_by = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True
    )
    edited_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return (
            f"History of Message {self.message.id} "
            f"by {self.edited_by} at {self.edited_at}"
        )
