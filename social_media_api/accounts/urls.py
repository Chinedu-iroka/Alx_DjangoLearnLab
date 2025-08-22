from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register_user, name='register'),
    path('login/', views.login_user, name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('profile/', views.user_profile, name='profile'),

    path('follow/', views.follow_user, name='follow'),
    path('unfollow/', views.unfollow_user, name='unfollow'),
    path('following/', views.get_following, name='following'),
    path('followers/', views.get_followers, name='followers'),
    path('profile/<int:user_id>/', views.user_profile_with_follow_status, name='user-profile-detail'),

    path('follow/<int:user_id>/', views.follow_user, name='follow'),
    path('unfollow/<int:user_id>/', views.unfollow_user, name='unfollow'),

    path('users/', views.UserListView.as_view(), name='user-list'),
    path('users/search/', views.UserSearchView.as_view(), name='user-search'),
]