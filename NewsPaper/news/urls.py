from django.urls import path
# Импортируем созданное нами представление
from .views import (
   NewsList, NewsDetail, NewsSearch, ArticleList, ArticleDetail, NewsCreate, NewsEdit, NewsDelete, ArticleCreate,
   ArticleEdit, CategoryListView, subscribe, to_many_post
)

from django.views.decorators.cache import cache_page


urlpatterns = [
   path('', NewsList.as_view()),

   path('news/', NewsList.as_view(), name='news_list'),
   path('news/<int:pk>', NewsDetail.as_view(), name='a_news'),
   path('articles/', ArticleList.as_view(), name='articles_list'),
   path('articles/<int:pk>', ArticleDetail.as_view(), name='article'),
   path('news/search/', NewsSearch.as_view(), name='news_search'),

   path('news/create/', NewsCreate.as_view(), name='news_create'),
   path('news/<int:pk>/edit/', NewsEdit.as_view(), name='post_edit'),
   path('news/<int:pk>/delete/', NewsDelete.as_view(), name='post_delete'),

   path('articles/create/', ArticleCreate.as_view(), name='articles_create'),
   path('articles/<int:pk>/edit/', ArticleEdit.as_view(), name='post_edit'),
   path('articles/<int:pk>/delete/', ArticleEdit.as_view(), name='post_delete'),

   path('articles/<int:pk>/delete/', ArticleEdit.as_view(), name='post_delete'),
   path('categories/<int:pk>', CategoryListView.as_view(), name='category_list'),
   path('categories/<int:pk>/subscribe', subscribe, name='subscribe'),

   path('to_many_post/', to_many_post, name='to_many_post'),

   # path('', IndexView.as_view()),
]
