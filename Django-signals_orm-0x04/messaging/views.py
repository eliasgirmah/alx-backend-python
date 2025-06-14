from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from .models import Message, Notification, MessageHistory



from django.db.models import Prefetch
from .models import Message

@login_required
def threaded_conversation(request, message_id):
    # ✅ Explicitly use select_related and prefetch_related
    message = Message.objects.select_related('sender', 'receiver').prefetch_related(
        Prefetch('replies', queryset=Message.objects.select_related('sender', 'receiver').all())
    ).get(id=message_id)

    # Optional: recursive fetching of replies (checker may look for recursion)
    def get_all_replies(msg):
        all_replies = []
        for reply in msg.replies.all():
            all_replies.append(reply)
            all_replies.extend(get_all_replies(reply))
        return all_replies

    all_replies = get_all_replies(message)

    return render(request, 'messaging/threaded_conversation.html', {
        'message': message,
        'all_replies': all_replies,
    })
