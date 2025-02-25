from django.http import JsonResponse
from django.conf import settings

class AdminAPIKeyMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.path.startswith('/api/admin/'):
            api_key = request.headers.get('X-API-KEY')
            if api_key != settings.ADMIN_API_KEY:
                return JsonResponse({"error": "Unauthorized: Invalid API Key"}, status=403)

        return self.get_response(request)
