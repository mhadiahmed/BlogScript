from django.urls import path
from . import views

app_name = "comments"

urlpatterns = [
    path('', views.CommentListView.as_view(), name='list'),
    path('delete/<int:pk>/', views.CommentDeleteView.as_view(), name="delete"),
    path("change-status/<int:pk>/", views.change_comment_status, name="change_status")
]