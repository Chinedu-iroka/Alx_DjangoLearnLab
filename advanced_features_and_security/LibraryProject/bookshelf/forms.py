from django import forms
from .models import Book 
class SearchForm(forms.Form):
    title = forms.CharField(max_length=100)

class ExampleForm(forms.ModelForm):
    class Meta:
        model = Book  
        fields = ['title', 'author', 'description']