from rest_framework import viewsets, status
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from .models import Conversation, Message
from .serializers import ConversationSerializer, MessageSerializer
from rest_framework.permissions import IsAuthenticated
from .permissions import IsParticipantOfConversation

User = get_user_model()


class ConversationViewSet(viewsets.ViewSet):
    """
    Handles creating and listing conversations.
    Only authenticated users can access their own conversations.
    """
    permission_classes = [IsAuthenticated,IsParticipantOfConversation]

    def list(self, request):
        conversations = Conversation.objects.filter(participants=request.user)
        serializer = ConversationSerializer(conversations, many=True)
        return Response(serializer.data)

    def create(self, request):
        conversation = Conversation.objects.create()
        conversation.participants.add(request.user)

        
        participants_id = request.data.get("participants", [])
        if participants_id:
            users = User.objects.filter(id__in=participants_id)
            conversation.participants.add(*users)

        serializer = ConversationSerializer(conversation)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class MessageViewSet(viewsets.ViewSet):
    """
    Handles creating and listing messages inside conversations.
    Only participants of a conversation can send or view messages.
    """

    permission_classes = [IsAuthenticated,IsParticipantOfConversation]

    def list(self, request):
        conversation_id = request.query_params.get("conversation_id")
        if not conversation_id:
            return Response(
                {"error": "conversation_id query parameter is required."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if not Conversation.objects.filter(id=conversation_id, participants=request.user).exists():
            return Response(
                {"error": "Not authorized to view this conversation."},
                status=status.HTTP_403_FORBIDDEN,
            )

        messages = Message.objects.filter(conversation_id=conversation_id)
        serializer = MessageSerializer(messages, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request):
        serializer = MessageSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        conversation = serializer.validated_data.get("conversation")
        recipient = serializer.validated_data.get("recipient")

        
        if not conversation.participants.filter(id=request.user.id).exists():
            return Response(
                {"error": "Not authorized to send messages in this conversation."},
                status=status.HTTP_403_FORBIDDEN,
            )

      
        if not conversation.participants.filter(id=recipient.id).exists():
            return Response(
                {"error": "Recipient is not in this conversation."},
                status=status.HTTP_400_BAD_REQUEST,
            )

       
        message = Message.objects.create(
            conversation=conversation,
            sender=request.user,
            recipient=recipient,
            message_body=serializer.validated_data.get("message_body"),
        )

        output_serializer = MessageSerializer(message)
        return Response(output_serializer.data, status=status.HTTP_201_CREATED)
