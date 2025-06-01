from rest_framework import serializers
from .models import User, Conversation, Message

class UserSerializer(serializers.ModelSerializer):
    user_id = serializers.UUIDField(source='id', read_only=True)
    phone_number = serializers.CharField(required=False, allow_blank=True)
    first_name = serializers.CharField(required=False, allow_blank=True)
    last_name = serializers.CharField(required=False, allow_blank=True)

    class Meta:
        model = User
        fields = ['user_id', 'username', 'email', 'phone_number', 'first_name', 'last_name']
        read_only_fields = ['user_id']

class MessageSerializer(serializers.ModelSerializer):
    message_id = serializers.UUIDField(source='id', read_only=True)
    conversation = serializers.PrimaryKeyRelatedField(queryset=Conversation.objects.all())
    sender = UserSerializer(read_only=True)
    
    # Example of SerializerMethodField usage (e.g., return a snippet of the message)
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

class ConversationSerializer(serializers.ModelSerializer):
    conversation_id = serializers.UUIDField(source='id', read_only=True)
    participants = UserSerializer(many=True, read_only=True)
    sent_messages = MessageSerializer(many=True, read_only=True, source='sent_messages')

    # Example of SerializerMethodField to count messages
    message_count = serializers.SerializerMethodField()

    class Meta:
        model = Conversation
        fields = ['conversation_id', 'participants', 'created_at', 'sent_messages', 'message_count']
        read_only_fields = ['conversation_id', 'created_at']

    def get_message_count(self, obj):
        return obj.sent_messages.count()
