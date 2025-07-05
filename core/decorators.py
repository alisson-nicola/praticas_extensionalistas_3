from django.shortcuts import redirect
from django.contrib import messages
from functools import wraps

def permission_required(screen_name):
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            user = request.user

            if not user.is_authenticated:
                messages.error(request, "Você precisa estar autenticado para acessar esta página.")
                return redirect('core:home_view')

            if user.is_superuser or user.is_admin:
                return view_func(request, *args, **kwargs)

            if user.group and user.group.permissions.filter(name__iexact=screen_name).exists():
                return view_func(request, *args, **kwargs)

            messages.error(request, "Você não tem permissão para acessar esta página.")
            return redirect('core:home_view')
        return _wrapped_view
    return decorator
