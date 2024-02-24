from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, FormView
from .models import Post, UserCategory, PostCategory
from django.contrib.auth.models import User
from .filters import PostFilter
from .forms import PostForm
from django.shortcuts import render, HttpResponseRedirect
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives
from .passwords import host_password, login


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
        post = form.save(commit=False)
        post.author = self.request.user.author
        post.save()

        super().form_valid(form)

        category_id = form.cleaned_data['category']
        content = form.cleaned_data['content']
        subscriber_id_list = list(UserCategory.objects.filter(category__id__in=category_id).values_list('user', flat=True))
        # subscriber_id_list = [UserCategory.objects.get(category_id=category_id).user_id]
        # subscriber_id_list = [11]

        html_content = render_to_string(
            'a_news.html',
            {
                'post': post,
            }
        )

        if subscriber_id_list:
            for id_ in subscriber_id_list:
                user_name = User.objects.get(id=id_).username
                email = User.objects.get(id=id_).email
                if email:
                    msg = EmailMultiAlternatives(
                        subject=f'Здравствуй, {user_name}. Новая статья в твоём любимом разделе!',
                        body=content,
                        from_email='project-corp@yandex.ru',
                        to=[email],
                    )
                    msg.attach_alternative(html_content, "text/html")
                    msg.send()

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


class SubscribersView(CreateView):
    model = UserCategory
    # form_class = SubscribersForm
    template_name = 'subscribe.html'
    success_url = '/subscribe/'

    def form_valid(self, form):
        subscribers = form.save(commit=False)
        is_subscribed = UserCategory.objects.filter(category=form.instance.category, user=self.request.user).exists()
        self.request.session['subscriber_category'] = f'Вы успешно подписались на категорию "{form.instance.category.name}"'
        self.request.session['is_subscribed'] = is_subscribed
        if not is_subscribed:
            if self.request.method == 'POST':
                form.instance.user = self.request.user
            subscribers.save()
            send_mail(
                subject='Подписка на категорию',
                message=f'Вы подписались на новости из категории { form.instance.category }',
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[self.request.user.email],
            )
            return super().form_valid(form)
        return render(self.request, 'subscribe.html', context={'message': f'Вы уже подписаны на данную категорию "{form.instance.category}"', 'form': form})