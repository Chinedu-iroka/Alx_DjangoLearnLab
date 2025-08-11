from django.shortcuts import render

# Create your views here.
from .models import Post

def home(request):
    posts = Post.objects.all().order_by('-published_date')  # latest first
    return render(request, 'blog/home.html', {'posts': posts})