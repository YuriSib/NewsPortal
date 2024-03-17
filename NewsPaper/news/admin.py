from django.contrib import admin
from .models import Category, Post
import django.db.models.fields.related as F


class PostAdmin(admin.ModelAdmin):
    # list_display — это список или кортеж со всеми полями, которые вы хотите видеть в таблице с товарами
    # list_display = ('name', 'price') # генерируем список имён всех полей для более красивого отображения
    list_display = []
    for field in Post._meta.get_fields():
        if type(field) == F.ManyToManyField or type(field) == F.ManyToOneRel:
            continue
        print(field.name, type(field.name), field, type(field))
        list_display.append(field.name)
    list_filter = ('title', 'author')  # добавляем примитивные фильтры в нашу админку
    search_fields = ('title', 'author')  # тут всё очень похоже на фильтры из запросов в базу


admin.site.register(Category)
admin.site.register(Post, PostAdmin)
