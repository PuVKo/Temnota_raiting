from django.utils.deprecation import MiddlewareMixin
from django.shortcuts import redirect

class DeviceDetectionMiddleware(MiddlewareMixin):
    def process_request(self, request):
        is_mobile = False
        user_agent = request.META.get('HTTP_USER_AGENT', '').lower()
        if 'mobile' in user_agent:
            is_mobile = True
        request.is_mobile = is_mobile
        return None