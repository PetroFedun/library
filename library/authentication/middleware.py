# authentication/middleware.py
from .views import get_logged_user_id
from .models import CustomUser

class SetLoggedInUserMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        request.logged_user_id = get_logged_user_id(request)
        if request.logged_user_id != -1:
            request.logged_user_role = CustomUser.get_by_id(request.logged_user_id).role
        response = self.get_response(request)
        return response
