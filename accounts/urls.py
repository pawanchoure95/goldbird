from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('profile/edit/', views.profile_edit, name='profile_edit'),
    path('profile/', views.profile, name='profile'),
    path('profile/<str:username>/', views.profile_view, name='profile_view'),
    path('search/', views.search_users, name='search'),
    path('chat/', views.chat_home, name='chat_home'),
    path('chat/<str:username>/', views.chat_room, name='chat_room'),
    path('chat-api/token/', views.chat_firebase_token, name='chat_firebase_token'),
    path('like/<str:username>/', views.like_user, name='like_user'),
]
