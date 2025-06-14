from django.test import TestCase
from django.contrib.auth.models import User
from .models import Message, Notification, MessageHistory

class UserDeletionSignalTest(TestCase):
    def test_user_deletion_cleans_related_data(self):
        user = User.objects.create_user(username="john", password="test")
        msg = Message.objects.create(sender=user, receiver=user, content="hi")
        Notification.objects.create(user=user, message=msg)
        MessageHistory.objects.create(message=msg, old_content="old", edited_by=user)

        user.delete()

        self.assertFalse(Message.objects.exists())
        self.assertFalse(Notification.objects.exists())
        self.assertFalse(MessageHistory.objects.exists())
