import json
from django.http import JsonResponse
from django.core.cache import cache
from django.conf import settings

def get_client_ip(request):
    xff = request.META.get('HTTP_X_FORWARDED_FOR')
    if xff:
        return xff.split(',')[0].strip()
    return request.META.get('REMOTE_ADDR')

class OffensiveLanguageMiddleware:
    """
    - Rate-limits POST requests to messages endpoint by IP.
    - Blocks messages containing offensive words (simple substring match).
    """

    def __init__(self, get_response):
        self.get_response = get_response
        self.limit = getattr(settings, 'MESSAGE_RATE_LIMIT', 5)
        self.window = getattr(settings, 'MESSAGE_RATE_WINDOW', 60)
        self.offensive = set(getattr(settings, 'OFFENSIVE_WORDS', []))

    def __call__(self, request):
        path = request.path
        if path.startswith('/api/') and path.endswith('/messages/') and request.method == 'POST':
            ip = get_client_ip(request) or 'unknown'
            key = f"msg_count:{ip}"
            count = cache.get(key, 0)
            if count >= self.limit:
                return JsonResponse({'detail': 'Rate limit exceeded. Try again later.'}, status=429)

            # read JSON body safely
            try:
                body = request.body.decode('utf-8') or '{}'
                data = json.loads(body)
                message = (data.get('message_body') or '').lower()
            except Exception:
                return JsonResponse({'detail': 'Invalid JSON payload.'}, status=400)

            # check offensive words
            for bad in self.offensive:
                if bad in message:
                    return JsonResponse({'detail': 'Message contains offensive language.'}, status=400)

            # increment counter (simple approach)
            cache.set(key, count + 1, timeout=self.window)

        return self.get_response(request)
