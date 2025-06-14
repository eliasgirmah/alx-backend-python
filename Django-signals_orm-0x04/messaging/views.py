from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from django.db.models import Prefetch
from .models import Message

@login_required
def unread_inbox(request):
    """
    Display unread messages for the logged-in user.
    Uses the custom manager method AND explicit filter() with only() for optimization.
    """
    user = request.user
    
    # Using the custom manager method to get unread messages for user
    unread_messages = Message.unread.unread_for_user(user)
    
    # Additionally, explicitly filter and optimize with only()
    # (optional, since unread_for_user already uses filter and only)
    unread_messages = unread_messages.filter(receiver=user, read=False).only('id', 'sender', 'timestamp', 'content')

    return render(request, 'messaging/unread_inbox.html', {
        'unread_messages': unread_messages,
    })


@login_required
def threaded_conversation(request, message_id):
    """
    Display a message and all its threaded replies recursively,
    optimized with select_related and prefetch_related.
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
