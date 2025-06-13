from django.contrib.auth.models import User
from messaging.models import Message, Notification

sender = User.objects.create_user(username='alice', password='testpass')
receiver = User.objects.create_user(username='bob', password='testpass')

# Create a message
msg = Message.objects.create(sender=sender, receiver=receiver, content='Hello Bob!')

# Check notification
Notification.objects.filter(user=receiver).first()
