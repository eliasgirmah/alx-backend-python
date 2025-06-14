from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from .models import Message, Notification, MessageHistory

@login_required
def inbox(request):
    """Show all messages received by the user."""
    messages = Message.objects.filter(receiver=request.user).order_by('-timestamp')
    return render(request, 'messaging/inbox.html', {'messages': messages})

@login_required
def sent_messages(request):
    """Show all messages sent by the user."""
    messages = Message.objects.filter(sender=request.user).order_by('-timestamp')
    return render(request, 'messaging/sent.html', {'messages': messages})

@login_required
def view_message_history(request, message_id):
    """Show message edit history for a given message."""
    message = get_object_or_404(Message, id=message_id)
    history = message.history.all().order_by('-edited_at')
    return render(request, 'messaging/message_history.html', {
        'message': message,
        'history': history
    })

@login_required
def delete_user(request):
    """View to allow user to delete their account and all related data."""
    if request.method == "POST":
        user = request.user
        user.delete()
        return redirect('home')  # Redirect to homepage or goodbye page after deletion
    return render(request, 'messaging/delete_user_confirm.html')
