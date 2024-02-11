from django_filters import FilterSet
from .models import Post

# Создаем свой набор фильтров для модели Product.
# FilterSet, который мы наследуем,
# должен чем-то напомнить знакомые вам Django дженерики.


class PostFilter(FilterSet):

    class Meta:
        # В Meta классе мы должны указать Django модель,
        # в которой будем фильтровать записи.
        model = Post
        # В fields мы описываем по каким полям модели
        # будет производиться фильтрация.
        fields = {
            # поиск по названию
            'title': ['icontains'],
            # поиск по id автора (нужно переделать на фильтрацию по username)
            'author': ['exact'],
            # покажет объекты созданные позже указанной даты
            'time_create': ['month__gt'],
        }
