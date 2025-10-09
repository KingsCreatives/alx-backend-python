from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import get_user_model
from .models import Message

User = get_user_model()

# Create your views here.
def delete_user(request, user_id):
    user_to_delete = get_object_or_404(User,pk=user_id)

    user_to_delete.delete()

    return redirect('home')


def get_optimized_messages():
    
    top_level_messages = Message.objects.filter(parent_message__isnull=True)

    optimized_query = top_level_messages.select_related(
        'sender',
        'receiver',
        'parent_message__sender'
    )

    optimized_query = optimized_query.prefetch_related(
        'messaging_replies',
        'messaging_replies__sender'
    )

    return optimized_query


def get_message_thread(message_id):
    
    root = Message.objects.select_related('sender', 'receiver').get(pk=message_id)

    level_1_replies = root.messaging_replies.all().select_related('sender', 'receiver')

    level_2_replies = Message.objects.filter(
        parent_message__in=level_1_replies
    ).select_related('sender', 'receiver')

    return {
        'root': root,
        'level_1' : level_1_replies,
        'level_2' : level_2_replies
    }
