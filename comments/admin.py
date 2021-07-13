from django.contrib import admin

from .models import Comment


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'post', 'created', 'status')
    list_filter = ('status', 'created', 'updated')
    search_fields = ('name', 'email', 'body')
