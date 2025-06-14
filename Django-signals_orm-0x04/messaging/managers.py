from django.db import models


class UnreadMessagesManager(models.Manager):
    """
    Custom manager to get unread messages for a specific user,
    optimized to only fetch necessary fields.
    """

    def unread_for_user(self, user):
        return (
            self.get_queryset()
            .filter(receiver=user, read=False)
            .only('id', 'sender', 'timestamp', 'content')
        )
