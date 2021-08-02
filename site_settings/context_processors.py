from .models import Page, SiteSetting, Option
from django.shortcuts import get_object_or_404
def site_settings(request):
    try:
        pag_es =  Page.objects.filter(status="active")
    except:
        pag_es = None
        
    try:
        site_settings=SiteSetting.objects.get(id=1) ,
    except:
        site_settings = None
        
    try:
        Options=Option.objects.get(id=1)
    except:
        Options= None
        
    return {
        "pag_es":pag_es,
        "site_settings":site_settings,
        "options":Options
        }