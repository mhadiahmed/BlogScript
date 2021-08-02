from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.urls import include, path, re_path
from site_settings import views

from .staticfiles_urlpatterns_media import staticfiles_urlpatterns_media

urlpatterns = [
    path('admin/', admin.site.urls),
    path('dashboard/', include('dashboard.urls')),
    path('authors/', include('authors.urls')),
    path('settings/', include('site_settings.urls')),
    path('comments/', include('comments.urls')),
    path('ckeditor/', include('ckeditor_uploader.urls')),
    path('posts/', include('posts.urls')),
    path('site/<path:url>/', views.page, name='site_settings.views.page'),
    path('', include('core.urls')),
]


urlpatterns += staticfiles_urlpatterns()
urlpatterns += staticfiles_urlpatterns_media()
