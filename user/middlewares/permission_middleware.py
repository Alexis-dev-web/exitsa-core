# middleware.py
from functools import wraps
from rest_framework import status as api_status
from django.http import HttpResponse
from utils.error_messages import messages

from django.contrib.auth.models import Permission


def permission_required(permission_code):
    def decorator(view_function):
        @wraps(view_function)
        def _wrapped_view(self, request, *args, **kwargs):
            user = request.user

            if not user.is_superuser or not user.has_perm(permission_code):
                permission = Permission.objects.get(codename=permission_code)

                if not user.groups.filter(permissions=permission).exists():
                    return HttpResponse({'message': messages['permission_denied']}, status=api_status.HTTP_403_FORBIDDEN)

            return view_function(self, request, *args, **kwargs)
        return _wrapped_view
    return decorator
