from django.contrib import admin
from .models import SiteSetting, Option, Page
# Register your models here.

class PageAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {'fields': ('url', 'title', 'sites','content')}),
        (('Advanced options'), {
            'fields': ('template_name',),
        }),
    )
    list_display = ('url', 'title')
    list_filter = ('sites', 'registration_required')
    search_fields = ('url', 'title')

admin.site.register(Page, PageAdmin)
admin.site.register(SiteSetting)
admin.site.register(Option)
