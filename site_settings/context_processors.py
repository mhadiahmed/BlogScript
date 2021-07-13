from .models import SiteSetting, Option
from django.shortcuts import get_object_or_404
def site_settings(request):
    return {
        'site_settings':get_object_or_404(SiteSetting,id=1),
        'options':get_object_or_404(Option,id=1)
        }