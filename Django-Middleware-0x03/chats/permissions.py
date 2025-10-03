from rest_framework import permissions
from .models import Conversation, Message

class IsOwner(permissions.BasePermission):
    
    def has_object_permission(self, request, view, obj):
        return obj.owner == request.user

class IsParticipantOfConversation(permissions.BasePermission):
    
    def has_object_permission(self, request, view, obj):
        if isinstance(obj, Conversation):
            return request.user in obj.participants.all()
        
        if isinstance(obj, Message):
            return request.user in obj.conversation.participants.all()
        
        return False