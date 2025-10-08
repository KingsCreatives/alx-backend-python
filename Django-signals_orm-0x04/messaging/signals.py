from django.db.models.signals import post_save, pre_save, post_delete
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from .models import Message, Notification, MessageHistory


User = get_user_model()

@receiver(post_save,sender=Message)
def create_notification_on_new_message(sender, instance, created, **kwargs):
    
    if created:
        receiver_user = instance.receiver

        Notification.objects.create(
            user=receiver_user,
            message=instance,
            is_read=False
        )


@receiver(pre_save,sender=Message)
def log_message_edits(sender, instance, **kwargs):
    
    if instance.pk:
        try:
            old_message = Message.objects.get(pk=instance.pk)
        
        except Message.DoesNotExist:
            return
        
        if old_message.context != instance.content:
            MessageHistory.objects.create(
                message = instance,
                old_content = old_message.content,
            )

            instance.edited = True

@receiver(post_delete,sender=User)
def log_user_deletion(sender, instance,**kwargs):
    print(f"Audit Log: User ID {instance.pk} ({instance.username}) was permanently deleted")