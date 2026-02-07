from django.contrib.auth import logout
from django.shortcuts import redirect

class BanCheckMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        user = request.user

        if user.is_authenticated and (getattr(user, 'is_banned', False) or not user.is_active):
            logout(request)
            return redirect('login')
        
        return self.get_response(request)