import django_filters
from .models import Message

class MessageFilter(django_filters.FilterSet):
    start_date = django_filters.DateTimeFilter(field_name="sent_at", lookup_expr="gte")
    end_date = django_filters.DateTimeFilter(field_name="sent_at", lookup_expr="lte")
    sender = django_filters.UUIDFilter(field_name="sender__id")
    recipient = django_filters.UUIDFilter(field_name="recipient__id")

    class Meta:
        model = Message
        fields = ["sender", "recipient", "start_date", "end_date"]
