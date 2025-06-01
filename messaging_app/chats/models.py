from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.
class User(AbstractUser):
    bio=models.TextField(max_length=500, blank=True, null=True)
    
    def __str__(self):
        return self.username
class conversation(models.Model):
    participants= models.ManyToManyField(User, related_name="conversations")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"conversation {self.id}"
    
class message(models.Model):
    conversation = models.ForeignKey(conversation, on_delete=models.CASCADE, related_name="sent_messages")
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name="messages")
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"From {self.sender.username}: {self.content[:20]}"
    

    

