# chats/middleware/request_logging.py
import logging, time
from datetime import datetime

logger = logging.getLogger('requests_logger')

class RequestLoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        start = time.time()
        user = getattr(request, 'user', None)
        username = None
        try:
            username = request.user.email if getattr(user, 'is_authenticated', False) else 'Anonymous'
        except Exception:
            username = 'Anonymous'

        logger.info(f"{datetime.now().isoformat()} - User: {username} - Method: {request.method} - Path: {request.get_full_path()}")

        response = self.get_response(request)

        duration = time.time() - start
        logger.info(f"{datetime.now().isoformat()} - User: {username} - Path: {request.get_full_path()} - Status: {response.status_code} - Duration: {duration:.3f}s")

        return response
