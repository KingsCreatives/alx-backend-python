import logging
from datetime import datetime, timedelta
from django.http import JsonResponse

# -------------------------------
# 1. Logging User Requests
# -------------------------------

class RequestLoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        logging.basicConfig(
            filename="requests.log",
            level=logging.INFO,
            format="%(asctime)s - %(message)s",
        )

    def __call__(self, request):
        user = getattr(request, "user", None)
        try:
            username = (
                request.user.email if getattr(user, "is_authenticated", False)
                else "Anonymous"
            )
        except Exception:
            username = "Anonymous"

        logging.info(f"User: {username} - Path: {request.path}")
        return self.get_response(request)


# -------------------------------
# 2. Restrict Chat Access by Time
# -------------------------------

class RestrictAccessByTimeMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.start_hour = 6
        self.end_hour = 21    

    def __call__(self, request):
        now = datetime.now()
        hour = now.hour

        if not (self.start_hour <= hour < self.end_hour):
            return JsonResponse(
                {"detail": "Chat access is restricted at this time."},
                status=403
            )

        return self.get_response(request)


# -------------------------------
# 3. Offensive Language / Message Rate Limit
# -------------------------------

class OffensiveLanguageMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.requests_per_ip = {}  # {ip: [(timestamps), ...]}
        self.limit = 5             # max messages per minute
        self.time_window = timedelta(minutes=1)

    def __call__(self, request):
        if request.method == "POST" and request.path.startswith("/chats/"):
            ip = self.get_client_ip(request)
            now = datetime.now()

            if ip not in self.requests_per_ip:
                self.requests_per_ip[ip] = []

            # keep only requests in the last minute
            self.requests_per_ip[ip] = [
                t for t in self.requests_per_ip[ip]
                if now - t < self.time_window
            ]

            if len(self.requests_per_ip[ip]) >= self.limit:
                return JsonResponse(
                    {"detail": "Rate limit exceeded. Try again later."},
                    status=429
                )

            self.requests_per_ip[ip].append(now)

        return self.get_response(request)

    def get_client_ip(self, request):
        x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
        if x_forwarded_for:
            return x_forwarded_for.split(",")[0].strip()
        return request.META.get("REMOTE_ADDR", "")


# -------------------------------
# 4. Role Permission Middleware
# -------------------------------

class RolePermissionMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.restricted_paths = ["/chats/admin/"]  # example admin path

    def __call__(self, request):
        user = getattr(request, "user", None)

        # If accessing restricted paths
        if any(request.path.startswith(p) for p in self.restricted_paths):
            if not user or not getattr(user, "is_authenticated", False):
                return JsonResponse(
                    {"detail": "Authentication required."},
                    status=403
                )

            # Check role (assuming user model has 'role' field)
            if getattr(user, "role", "BASIC") not in ["ADMIN", "MODERATOR"]:
                return JsonResponse(
                    {"detail": "You do not have permission to access this resource."},
                    status=403
                )

        return self.get_response(request)
