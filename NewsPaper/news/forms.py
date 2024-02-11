from django import forms
from .models import Post


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'content', 'time_create']
        widgets = {
            'time_create': forms.DateInput(attrs={'type': 'date'}),
        }
