from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from django.db.models import Prefetch
from .models import Message

@login_required
def unread_inbox(request):
    """
    View to display unread messages for the logged-in user.
    Uses custom manager to filter unread messages and optimizes query with .only().
    """
    user = request.user
    unread_messages = Message.unread.unread_for_user(user)
    return render(request, 'messaging/unread_inbox.html', {
        'unread_messages': unread_messages,
    })

@login_required
def threaded_conversation(request, message_id):
    """
    View to display a message and all its threaded replies recursively.
    Uses select_related and prefetch_related to optimize DB queries.
    """
    message = get_object_or_404(
        Message.objects.select_related('sender', 'receiver').prefetch_related(
            Prefetch(
                'replies',
                queryset=Message.objects.select_related('sender', 'receiver').all()
            )
        ),
        id=message_id
    )

    def get_all_replies(msg):
        """
        Recursively collect all replies to a message in a flat list.
        """
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
