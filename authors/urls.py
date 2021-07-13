from django.contrib.auth import views as auth_view
from django.urls import path

from . import views

app_name = "authors"

urlpatterns = [
    path('', views.AuthorListView.as_view(), name='authors'),
    path('login/',auth_view.LoginView.as_view(), name="login"),
    path('logout/',auth_view.LogoutView.as_view(), name="logout"),
    path('add/', views.add_author, name='add_author'),
    path('edit/<int:pk>/', views.AuthorEditView.as_view(), name="edit_author"),
    path('delete/<int:pk>/', views.AuthorDeleteView.as_view(), name="delete_author"),
    
    # password rest
    path('password_reset/', views.PasswordResetView.as_view(), name="password_reset"),
    path('password_reset/done/', auth_view.PasswordResetDoneView.as_view(), name="password_reset_done"),
    path('reset/<uidb64>/<token>/', views.PasswordResetConfirmView.as_view(), name="password_reset_confirm"),
    path('reset_password_complete/', auth_view.PasswordResetCompleteView  .as_view(), name="password_reset_complete"),
]
