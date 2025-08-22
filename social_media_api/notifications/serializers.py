from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType
from .models import Notification

User = get_user_model()

class UserSimpleSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'first_name', 'last_name')

class NotificationSerializer(serializers.ModelSerializer):
    actor = UserSimpleSerializer(read_only=True)
    target_object = serializers.SerializerMethodField()
    
    class Meta:
        model = Notification
        fields = ('id', 'recipient', 'actor', 'verb', 'read', 'timestamp', 'target_object')
        read_only_fields = ('id', 'timestamp')
    
    def get_target_object(self, obj):
        if obj.target:
            # You can customize this based on your target models
            if hasattr(obj.target, 'title'):  # For posts
                return {'type': 'post', 'title': obj.target.title, 'id': obj.target.id}
            elif hasattr(obj.target, 'content'):  # For comments
                return {'type': 'comment', 'content': obj.target.content[:50], 'id': obj.target.id}
        return None