from django.db import models
from django.contrib.auth import get_user_model


User = get_user_model()

# Create your models here.
class Message(models.Model):
    sender = models.ForeignKey(User, related_name='messaging_sent_messages', on_delete=models.CASCADE)
    receiver = models.ForeignKey(User, name='messaging_recived_messages', on_delete=models.CASCADE)
    context = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    edited = models.BooleanField(default=False)

    class Meta:
        ordering = ['-timestamp']

    def __str__(self):
        return f"From {self.sender.username} to {self.receiver.username}"


class Notification(models.Model):
    user = models.ForeignKey(User, related_name='messaging_notifications', on_delete=models.CASCADE)
    message = models.ForeignKey(Message, on_delete=models.CASCADE)
    is_read = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"New message notification for {self.user.username}"
    

class MessageHistory(models.Model):
    message = models.ForeignKey(Message, related_name='messaging_history', on_delete=models.CASCADE)
    old_content = models.TextField()
    edited_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"History of Message ID {self.message_id} edited at {self.edited_at.strftime('%Y-%m-%d %H:%M')}"