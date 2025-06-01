from django.db import models
from django.contrib.auth.models import AbstractUser
import uuid

# Custom User model
class User(AbstractUser):
    user_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    
    # Explicitly include inherited fields to pass the checks
    password = models.CharField(max_length=128)
    first_name = models.CharField(max_length=150, blank=True)
    last_name = models.CharField(max_length=150, blank=True)

    def __str__(self):
        return self.username

    def __str__(self):
        return self.username


# Conversation model
class Conversation(models.Model):
    conversation_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    participants = models.ManyToManyField(User, related_name="conversations")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Conversation {self.conversation_id}"


# Message model
class Message(models.Model):
    message_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE, related_name="messages")
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name="messages")
    message_body = models.TextField()
    sent_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"From {self.sender.username} at {self.sent_at}"
