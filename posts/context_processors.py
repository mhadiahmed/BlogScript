from .models import Categories


def category(request):
    try:
        category = Categories.objects.filter(status="active")
    except:
        category = None
    
    return{
        "category":category
    }