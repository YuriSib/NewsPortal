from django import forms
from .models import Post


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'content', 'category']
        widgets = {
            'time_create': forms.DateInput(attrs={'type': 'date'}),
        }
