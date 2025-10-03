from django.http import JsonResponse
from django.conf import settings
from datetime import datetime
import pytz

class RestrictAccessByTimeMiddleware:
    """
    Block chat API access outside allowed hours.
    By default, ALLOWED_CHAT_HOURS (settings) defines start and end (inclusive).
    """

    def __init__(self, get_response):
        self.get_response = get_response
        self.start_hour = settings.ALLOWED_CHAT_HOURS.get('start', 6)
        self.end_hour = settings.ALLOWED_CHAT_HOURS.get('end', 21)

    def __call__(self, request):
       
        path = request.path
        if path.startswith('/api/') and ('conversations' in path or 'messages' in path):
            now = datetime.now(pytz.utc).astimezone()
            hour = now.hour
            
            if not (self.start_hour <= hour < self.end_hour):
                return JsonResponse({'detail': 'Chat access is restricted at this time.'}, status=403)
        return self.get_response(request)
