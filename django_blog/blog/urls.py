from django.urls import path
from blog import views

urlpatterns = [
    path('', views.home, name='home'),
    path('posts/', views.posts, name='posts'), 
    path('login/', views.CustomLoginView.as_view(), name='login'),
    path('logout/', views.CustomLogoutView.as_view(), name='logout'),
    path('register/', views.register, name='register'),
    path('profile/', views.profile, name='profile'),
    path('posts/', views.posts, name='posts'),


    path('', views.PostListView.as_view(), name='home'),   # optional: home as posts list
    path('posts/', views.PostListView.as_view(), name='posts'),
    path('posts/new/', views.PostCreateView.as_view(), name='post-create'),
    path('posts/<int:pk>/', views.PostDetailView.as_view(), name='post-detail'),
    path('posts/<int:pk>/edit/', views.PostUpdateView.as_view(), name='post-update'),
    path('posts/<int:pk>/delete/', views.PostDeleteView.as_view(), name='post-delete'),
]