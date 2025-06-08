# chats/middleware.py

from datetime import datetime
import logging

# Configure logger
logger = logging.getLogger("request_logger")
handler = logging.FileHandler("requests.log")
formatter = logging.Formatter('%(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.setLevel(logging.INFO)

class RequestLoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        user = request.user if request.user.is_authenticated else 'Anonymous'
        log_entry = f"{datetime.now()} - User: {user} - Path: {request.path}"
        logger.info(log_entry)

        response = self.get_response(request)
        return response
# chats/middleware.py

from datetime import datetime
from django.http import HttpResponseForbidden


class RestrictAccessByTimeMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        now = datetime.now()
        current_hour = now.hour

        # Allow access only between 18:00 (6PM) and 21:00 (9PM)
        if current_hour < 18 or current_hour >= 21:
            return HttpResponseForbidden("Chat access is only allowed between 6PM and 9PM.")

        return self.get_response(request)

import time
from collections import defaultdict
from django.http import HttpResponseForbidden

class OffensiveLanguageMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.request_logs = defaultdict(list)  # {ip: [timestamps]}

    def __call__(self, request):
        # Only limit POST requests (like sending a chat message)
        if request.method == 'POST':
            ip = self.get_client_ip(request)
            now = time.time()

            # Remove timestamps older than 60 seconds
            self.request_logs[ip] = [t for t in self.request_logs[ip] if now - t < 60]

            if len(self.request_logs[ip]) >= 5:
                return HttpResponseForbidden("Rate limit exceeded. Only 5 messages per minute allowed.")

            # Log the new request
            self.request_logs[ip].append(now)

        return self.get_response(request)

    def get_client_ip(self, request):
        """Get client IP address from request headers."""
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip

from django.http import JsonResponse

class RolepermissionMiddleware:  # ✅ Match exactly!
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if not request.user.is_authenticated:
            return JsonResponse({'error': 'Authentication required'}, status=403)

        allowed_roles = ['admin', 'moderator']
        user_role = getattr(request.user, 'role', None)

        if user_role not in allowed_roles:
            return JsonResponse({'error': 'Forbidden: Insufficient role'}, status=403)

        return self.get_response(request)
