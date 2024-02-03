from django.urls import path
# Импортируем созданное нами представление
from .views import NewsList, NewsDetail, ArticleList, ArticleDetail


urlpatterns = [
   path('news/', NewsList.as_view()),
   path('news/<int:pk>', NewsDetail.as_view()),
   path('articles/', ArticleList.as_view()),
   path('articles/<int:pk>', ArticleDetail.as_view()),
]
