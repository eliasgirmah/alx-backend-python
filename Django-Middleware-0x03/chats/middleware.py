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
