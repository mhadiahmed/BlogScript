from django.urls import path,re_path
from . import views
from django.contrib.auth.views import LoginView,LogoutView
app_name = "core"

urlpatterns = [
    path('', views.PostListViewFront.as_view(), name="list"),
    path('login/',LoginView.as_view(), name="login"),
    path('logout/',LogoutView.as_view(), name="logout"),
    path('category/<str:slug>/', views.CategoryPostListView.as_view(), name="category"),
    re_path(r'(?P<slug>[A-z\d\-]+)/$', views.PostDetailView.as_view(), name="detail"),
]