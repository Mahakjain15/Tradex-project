from django.urls import path
from . import views

app_name = 'users'

urlpatterns = [
    path('register/',           views.register,     name='register'),
    path('login/',              views.user_login,   name='login'),
    path('logout/',             views.user_logout,  name='logout'),
    path('feed/',               views.feed,         name='feed'),
    path('post/new/',           views.create_post,  name='create_post'),
    path('post/<int:pk>/delete/', views.delete_post, name='delete_post'),
    path('profile/<str:username>/', views.profile,  name='profile'),
    path('profile/edit/',       views.edit_profile, name='edit_profile'),
]
