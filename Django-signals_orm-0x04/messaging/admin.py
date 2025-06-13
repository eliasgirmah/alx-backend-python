from django.contrib import admin
from .models import Message, MessageHistory, Notification

admin.site.register(Message)
admin.site.register(Notification)
admin.site.register(MessageHistory)  # ✅ Register history model
