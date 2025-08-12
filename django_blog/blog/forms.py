from django import forms
from .models import Post
from .models import Comment
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'content']
        widgets = {
            'title': forms.TextInput(attrs={'placeholder': 'Post title'}),
            'content': forms.Textarea(attrs={'rows': 10, 'placeholder': 'Write your post...'}),
        }

class CommentForm(forms.ModelForm):
    content = forms.CharField(widget=forms.Textarea(attrs={'rows':4, 'placeholder': 'Add your comment...'}), label='')

    class Meta:
        model = Comment
        fields = ['content']