from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Post
from .filters import PostFilter
from .forms import PostForm
from django.shortcuts import render, HttpResponseRedirect
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin


class NewsList(ListView):
    model = Post
    ordering = 'time_create'

    # queryset = Post.objects.order_by('time_create')

    template_name = 'news.html'
    context_object_name = 'News'
    paginate_by = 2

    def get_queryset(self):
        queryset = Post.objects.filter(write_type='NE').order_by('-time_create')
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_not_authors'] = not self.request.user.groups.filter(name='authors').exists()
        return context


class NewsSearch(ListView):
    model = Post
    template_name = 'search.html'
    context_object_name = 'Search'
    paginate_by = 2

    def get_queryset(self):
        # Получаем обычный запрос
        queryset = super().get_queryset()
        # Используем наш класс фильтрации.
        # self.request.GET содержит объект QueryDict, который мы рассматривали
        # в этом юните ранее.
        # Сохраняем нашу фильтрацию в объекте класса,
        # чтобы потом добавить в контекст и использовать в шаблоне.
        self.filterset = PostFilter(self.request.GET, queryset)
        # Возвращаем из функции отфильтрованный список товаров
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Добавляем в контекст объект фильтрации.
        context['filterset'] = self.filterset
        return context


class NewsDetail(DetailView):
    # Модель всё та же, но мы хотим получать информацию по отдельному товару
    model = Post
    # Используем другой шаблон — a_news.html
    template_name = 'a_news.html'
    # Название объекта, в котором будет выбранный пользователем продукт
    context_object_name = 'A_news'


class ArticleList(ListView):
    model = Post
    ordering = 'time_create'

    # queryset = Post.objects.order_by('time_create')

    template_name = 'articles.html'
    context_object_name = 'Articles'

    def get_queryset(self):
        queryset = Post.objects.filter(write_type='AR').order_by('-time_create')
        return queryset


class ArticleDetail(DetailView):
    model = Post
    template_name = 'article.html'
    context_object_name = 'Article'

    def get_queryset(self):
        queryset = Post.objects.filter(write_type='AR')
        return queryset


class NewsCreate(PermissionRequiredMixin, CreateView):
    permission_required = ('news.add_post',)
    form_class = PostForm
    model = Post
    template_name = 'post_edit.html'
    success_url = reverse_lazy('news_list')

    def form_valid(self, form):
        form.instance.write_type = 'NE'
        return super().form_valid(form)


class NewsEdit(PermissionRequiredMixin, LoginRequiredMixin, UpdateView):
    permission_required = ('news.change_post',)
    form_class = PostForm
    model = Post
    template_name = 'post_edit.html'
    success_url = reverse_lazy('news_list')


class NewsDelete(PermissionRequiredMixin, DeleteView):
    permission_required = ('news.add_post',)
    model = Post
    template_name = 'post_delete.html'
    success_url = reverse_lazy('news_list')


class ArticleCreate(PermissionRequiredMixin, CreateView):
    permission_required = ('news.delete_post',)
    form_class = PostForm
    model = Post
    template_name = 'post_edit.html'
    success_url = reverse_lazy('news_list')

    def form_valid(self, form):
        form.instance.write_type = 'AR'
        return super().form_valid(form)


class ArticleEdit(PermissionRequiredMixin, LoginRequiredMixin, UpdateView):
    permission_required = ('news.change_post',)
    form_class = PostForm
    model = Post
    template_name = 'post_edit.html'
    success_url = reverse_lazy('news_list')


class ArticleDelete(PermissionRequiredMixin, DeleteView):
    permission_required = ('news.delete_post',)
    model = Post
    template_name = 'post_delete.html'
    success_url = reverse_lazy('news_list')
