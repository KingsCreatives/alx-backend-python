from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Message, Notification


@receiver(post_save,sender=Message)
def create_notification_on_new_message(sender, instance, created, **kwargs):
    
    if created:
        receiver_user = instance.receiver

        Notification.objects.create(
            user=receiver_user,
            message=instance,
            is_read=False
        )