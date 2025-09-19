from rest_framework import viewsets
from rest_framework import status
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from .models import Conversation, Message
from .serializers import ConversationSerializer, MessageSerializer

# Create your views here.
User = get_user_model()

class ConversationViewSet(viewsets.ViewSet):
    def list(self, request):
        conversations = Conversation.objects.filter(participants=request.user)
        serializer = ConversationSerializer(conversations, many=True)
        return Response(serializer.data)
    
    def create(self, request):
        conversation = Conversation.objects.create()
        conversation.participants.add(request.user)

        participants_id = request.data.get('participants', [])
        if participants_id:
            users = User.objects.filter(id__in=participants_id)
            conversation.participants.add(*users)
        
        serializer = ConversationSerializer(conversation)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class MessageViewSet(viewsets.ViewSet):
    def list(self, request):
        conversation_id = request.query_params.get("conversation_id")

        if not conversation_id:
            return Response(
                {"error": "conversation_id query parameter is required."},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        messages = Message.objects.filter(conversation_id = conversation_id)
        serializer = MessageSerializer(messages, many=True)
        return Response(serializer.data, status=200)
    
    from rest_framework import status, viewsets
from rest_framework.response import Response

class MessageViewSet(viewsets.ViewSet):
    def create(self, request):
        serializer = MessageSerializer(data=request.data)

        
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        
        conversation_id = serializer.validated_data.get("conversation").id
        recipient_id = serializer.validated_data.get("recipient").id

        
        message = Message.objects.create(
            conversation_id=conversation_id,
            sender=request.user,  
            recipient_id=recipient_id,
            message_body=serializer.validated_data.get("message_body")
        )

        
        output_serializer = MessageSerializer(message)
        return Response(output_serializer.data, status=status.HTTP_201_CREATED)
