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

    class Meta:
        model = Message
        fields = ['message_id', 'conversation', 'sender', 'message_body', 'sent_at']
        read_only_fields = ['message_id', 'sent_at']

class ConversationSerializer(serializers.ModelSerializer):
    conversation_id = serializers.UUIDField(source='id', read_only=True)
    
    participants = UserSerializer(many=True, read_only=True)
    sent_messages = MessageSerializer(many=True, read_only=True, source='messages')

    class Meta:
        model = Conversation
        fields = ['conversation_id', 'participants', 'created_at']
        read_only_fields = ['conversation_id', 'created_at']