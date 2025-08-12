from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView, LogoutView
from .forms import RegisterForm
from .models import Post

# Create your views here.
from .models import Post

def home(request):
    return render(request, 'blog/base.html')

def posts(request):
    all_posts = Post.objects.all().order_by('-published_date')
    return render(request, 'blog/posts.html', {'posts': all_posts})

class CustomLoginView(LoginView):
    template_name = 'blog/login.html'

class CustomLogoutView(LogoutView):
    template_name = 'blog/logout.html'

def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('profile')
    else:
        form = RegisterForm()
    return render(request, 'blog/register.html', {'form': form})

@login_required
def profile(request):
    if request.method == 'POST':
        request.user.email = request.POST.get('email')
        request.user.save()
        return redirect('profile')
    return render(request, 'blog/profile.html')

def posts(request):
    all_posts = Post.objects.all().order_by('-published_date')
    return render(request, 'blog/posts.html', {'posts': all_posts})