from django_filters import FilterSet, DateFilter, CharFilter, ModelChoiceFilter
from .models import Post
from django import forms
from django.contrib.auth.models import User
from django.db.models.query import QuerySet

# Создаем свой набор фильтров для модели Product.
# FilterSet, который мы наследуем,
# должен чем-то напомнить знакомые вам Django дженерики.


class PostFilter(FilterSet):
    # Для отображения календаря в фильтре, будем использовать класс DateFilter
    start_date = DateFilter(
        field_name='time_create',
        lookup_expr='gte',
        widget=forms.DateInput(attrs={'type': 'date'}),
        label='Дата публикации, с'
    )
    end_date = DateFilter(
        field_name='time_create',
        lookup_expr='lte',
        widget=forms.DateInput(attrs={'type': 'date'}),
        label='Дата публикации, до'
    )
    title = CharFilter(lookup_expr='icontains', label='Заголовок')

    class Meta:
        # В Meta классе мы должны указать Django модель,
        # в которой будем фильтровать записи.
        model = Post
        # В fields мы описываем по каким полям модели
        # будет производиться фильтрация.
        fields = {
            # поиск по id автора (нужно переделать на фильтрацию по username)
            'author': ['exact'],
        }

