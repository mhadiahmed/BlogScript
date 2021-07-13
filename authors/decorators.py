from django.http import HttpResponse
# from django.shortcuts import redirect


def allowed_users(allowed_roles=[]):
    def decorator(view_func):
        def wrapper_func(request, *args, **kwargs):
            if request.user.status == "active":
                role = request.user.role.role_name
                if role in allowed_roles:
                    return view_func(request, *args, *kwargs)
                else:
                    return HttpResponse("you are not allowed to see this page.")
        return wrapper_func
    return decorator