from django.http import JsonResponse

class RolePermissionMiddleware:
    """
    Deny access to certain endpoints for users who are not admin.
    """

    def __init__(self, get_response):
        self.get_response = get_response
        self.admin_roles = ('admin', 'moderator')

    def __call__(self, request):
        path = request.path
        user = getattr(request, 'user', None)

        if path.startswith('/api/') and 'messages' in path and request.method == 'DELETE':
            if not (getattr(user, 'is_authenticated', False) and getattr(user, 'role', None) in self.admin_roles):
                return JsonResponse({'detail': 'You do not have permission to delete messages.'}, status=403)

        if '/admin-only/' in path:
            if not (getattr(user, 'is_authenticated', False) and getattr(user, 'role', None) in self.admin_roles):
                return JsonResponse({'detail': 'Admin-only resource.'}, status=403)

        return self.get_response(request)
