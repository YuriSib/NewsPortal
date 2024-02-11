from django.urls import path
# Импортируем созданное нами представление
from .views import (
   NewsList, NewsDetail, NewsSearch, ArticleList, ArticleDetail, NewsCreate, NewsEdit, NewsDelete, ArticleCreate,
   ArticleEdit,
)


urlpatterns = [
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
]
