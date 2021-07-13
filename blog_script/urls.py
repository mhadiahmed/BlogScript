from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.urls import include, path

from .staticfiles_urlpatterns_media import staticfiles_urlpatterns_media

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('core.urls')),
    path('dashboard/', include('dashboard.urls')),
    path('posts/', include('posts.urls')),
    path('authors/', include('authors.urls')),
    path('settings/', include('site_settings.urls')),
    path('comments/', include('comments.urls')),
    path('ckeditor/', include('ckeditor_uploader.urls')),
]
urlpatterns += staticfiles_urlpatterns()
urlpatterns += staticfiles_urlpatterns_media()
