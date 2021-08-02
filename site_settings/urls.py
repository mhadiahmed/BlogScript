from django.urls import path
from . import views

app_name = "settings"

urlpatterns=[
    path('<int:pk>/',views.SiteSettingsListView.as_view(), name="settings"),
    path('options/<int:pk>/',views.SiteOption.as_view(), name="options"),
    path('category/', views.CategoryListView.as_view(), name="list"),
    path('category/add/', views.CategoryCreateView.as_view(), name="add"),
    path('category/edit/<int:pk>/', views.CategoryUpdateView.as_view(), name="edit"),
    path('category/delete/<int:pk>/', views.CategoryDeleteView.as_view(), name="delete"),
    path('page/', views.PageListView.as_view(), name="page_list"),
    path('page/add/', views.PageCreateView.as_view(), name="page_add"),
    path('page/edit/<int:pk>/', views.PageUpdateView.as_view(), name="page_edit"),
    path('page/delete/<int:pk>/', views.PageDeleteView.as_view(), name="page_delete"),
]