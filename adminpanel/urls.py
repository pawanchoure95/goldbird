from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.admin_login, name='admin_login'),
    path('logout/', views.admin_logout, name='admin_logout'),
    path('dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('users/', views.admin_users, name='admin_users'),
    path('user/<int:user_id>/', views.admin_view_user, name='admin_user_detail'),
    path('toggle-user/<int:user_id>/', views.admin_toggle_user_status, name='admin_toggle_user'),
    path('delete-user/<int:user_id>/', views.admin_delete_user, name='admin_delete_user'),
]
