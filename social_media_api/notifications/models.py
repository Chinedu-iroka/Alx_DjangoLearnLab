from django.db import models

# Create your models here.

from django.contrib.auth import get_user_model
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType

User = get_user_model()

class Notification(models.Model):
    # Notification types
    FOLLOW = 'follow'
    LIKE = 'like'
    COMMENT = 'comment'
    MENTION = 'mention'
    
    NOTIFICATION_TYPES = [
        (FOLLOW, 'Follow'),
        (LIKE, 'Like'),
        (COMMENT, 'Comment'),
        (MENTION, 'Mention'),
    ]
    
    recipient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    actor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='acted_notifications')
    verb = models.CharField(max_length=20, choices=NOTIFICATION_TYPES)
    read = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)
    
    # Generic foreign key for the target object (post, comment, etc.)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, null=True, blank=True)
    object_id = models.PositiveIntegerField(null=True, blank=True)
    target = GenericForeignKey('content_type', 'object_id')
    
    class Meta:
        ordering = ['-timestamp']
    
    def __str__(self):
        return f"{self.actor.username} {self.verb} - {self.recipient.username}"
    
    def mark_as_read(self):
        self.read = True
        self.save()
    
    @classmethod
    def create_notification(cls, recipient, actor, verb, target=None):
        """Helper method to create notifications"""
        content_type = None
        object_id = None
        
        if target:
            content_type = ContentType.objects.get_for_model(target)
            object_id = target.id
        
        return cls.objects.create(
            recipient=recipient,
            actor=actor,
            verb=verb,
            content_type=content_type,
            object_id=object_id
        )