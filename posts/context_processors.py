from .models import Categories


def category(request):
    category = Categories.objects.filter(status="active")
    context = {
        "category":category
    }
    return context