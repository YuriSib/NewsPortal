from django.views.generic import ListView, DetailView
from .models import Post


class NewsList(ListView):
    model = Post
    ordering = 'title'
    template_name = 'news.html'
    context_object_name = 'News'

    def get_queryset(self):
        queryset = Post.objects.filter(write_type='NE')
        return queryset


class NewsDetail(DetailView):
    # Модель всё та же, но мы хотим получать информацию по отдельному товару
    model = Post
    # Используем другой шаблон — product.html
    template_name = 'a_news.html'
    # Название объекта, в котором будет выбранный пользователем продукт
    context_object_name = 'A_news'

    def get_queryset(self):
        queryset = Post.objects.filter(write_type='NE')
        return queryset
