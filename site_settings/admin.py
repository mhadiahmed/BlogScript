from django.contrib import admin
from .models import SiteSetting, Option
# Register your models here.

admin.site.register(SiteSetting)
admin.site.register(Option)