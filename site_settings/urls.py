from django.urls import path
from . import views

app_name = "settings"

urlpatterns=[
    path('<int:pk>/',views.SiteSettingsListView.as_view(), name="settings"),
    path('options/<int:pk>/',views.SiteOption.as_view(), name="options"),
    path('category/', views.CategoryListView.as_view(), name="list"),
    path('category/add/', views.CategoryCreateView.as_view(), name="add"),
    path('category/edit/<int:pk>/', views.CategoryUpdateView.as_view(), name="edit"),
    path('category/delete/<int:pk>', views.CategoryDeleteView.as_view(), name="delete"),
]