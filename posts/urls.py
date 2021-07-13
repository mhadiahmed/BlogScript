from django.urls import path
from . import views 

app_name = "posts"

urlpatterns = [
    path('', views.PostListView.as_view(), name="list"),
    path('add/', views.PostCreateView.as_view(), name="add"),
    path('edit/<int:pk>/', views.PostUpdateView.as_view(), name="edit"),
    path("delete/<int:pk>/", views.PostDeleteView.as_view(), name="delete"),
]