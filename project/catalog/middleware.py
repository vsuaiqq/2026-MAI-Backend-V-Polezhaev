import re

from django.conf import settings
from django.contrib.auth.views import redirect_to_login
from django.http import JsonResponse


class LoginRequiredMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.exempt_patterns = [
            re.compile(p) for p in getattr(settings, 'LOGIN_EXEMPT_URLS', [])
        ]

    def __call__(self, request):
        if request.user.is_authenticated:
            return self.get_response(request)

        path = request.path_info
        if any(p.match(path) for p in self.exempt_patterns):
            return self.get_response(request)

        if path.startswith('/api/'):
            return JsonResponse({'detail': 'Authentication required'}, status=401)

        return redirect_to_login(path, settings.LOGIN_URL)
