from django.http import HttpResponseForbidden


def allowed_users(allowed_roles=None):
    """
    Decorator to restrict access based on user roles.

    Parameters:
    - allowed_roles (list): List of roles allowed to access the view.

    Usage:
    @allowed_users(allowed_roles=['admin', 'manager'])
    def my_view(request):
        # Your view logic
    """
    if allowed_roles is None:
        allowed_roles = []

    def decorator(view_func):
        def wrapper_func(request, *args, **kwargs):
            if request.user.status == "active":
                role = request.user.role.role_name
                if role in allowed_roles:
                    return view_func(request, *args, **kwargs)
                else:
                    return HttpResponseForbidden(
                        "You are not allowed to see this page."
                    )
            else:
                # Consider handling the case when user status is not "active"
                return HttpResponseForbidden("Your account is not active.")

        return wrapper_func

    return decorator
