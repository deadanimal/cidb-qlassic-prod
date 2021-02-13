from django.http import HttpResponse
from django.shortcuts import redirect

def allowed_users(allowed_roles=[]):
    def decorator(view_func):
        def wrapper_func(request, *args, **kwargs):
            role = None
            exist = False
            role = request.user.role
            if role in allowed_roles:
                exist = True
            # group = request.user.groups.all()[0].name
            # if group in allowed_roles:
            if exist:
                return view_func(request, *args, **kwargs)
            else:
                return HttpResponse('You are not authorized to view this page')
        return wrapper_func
    return decorator
