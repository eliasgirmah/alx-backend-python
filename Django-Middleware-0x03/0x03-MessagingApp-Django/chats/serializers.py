from rest_framework import serializers
from .models import User, Conversation, Message


# ✅ User Serializer
class UserSerializer(serializers.ModelSerializer):
    user_id = serializers.UUIDField(read_only=True)

    class Meta:
        model = User
        fields = ['user_id', 'username', 'email', 'phone_number', 'first_name', 'last_name']
        read_only_fields = ['user_id']


# ✅ Message Serializer
class MessageSerializer(serializers.ModelSerializer):
    message_id = serializers.UUIDField(read_only=True)
    conversation = serializers.PrimaryKeyRelatedField(queryset=Conversation.objects.all())
    sender = UserSerializer(read_only=True)
    message_snippet = serializers.SerializerMethodField()

    class Meta:
        model = Message
        fields = ['message_id', 'conversation', 'sender', 'message_body', 'sent_at', 'message_snippet']
        read_only_fields = ['message_id', 'sent_at']

    def get_message_snippet(self, obj):
        return obj.message_body[:20] + "..." if len(obj.message_body) > 20 else obj.message_body

    def validate_message_body(self, value):
        if not value.strip():
            raise serializers.ValidationError("Message body cannot be empty or whitespace.")
        return value


# ✅ Conversation Serializer
class ConversationSerializer(serializers.ModelSerializer):
    conversation_id = serializers.UUIDField(read_only=True)
    participants = UserSerializer(many=True, read_only=True)
    sent_messages = MessageSerializer(many=True, read_only=True)  # ✅ FIXED: no source argument
    message_count = serializers.SerializerMethodField()

    class Meta:
        model = Conversation
        fields = ['conversation_id', 'participants', 'created_at', 'sent_messages', 'message_count']
        read_only_fields = ['conversation_id', 'created_at']

    def get_message_count(self, obj):
        return obj.sent_messages.count()
