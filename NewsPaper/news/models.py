from django.contrib.auth.models import User
from django.db import models
from django.db.models import Sum


class Author(models.Model):
    user = models.OneToOneField(User, on_delete=models.PROTECT, verbose_name='Имя')
    rating = models.IntegerField(default=0)

    def update_rating(self):
        rating_of_posts_by_author = Post.objects.filter(author=self).aggregate(Sum('rating'))['rating__sum'] * 3
        rating_of_posts_by_author = 0 if not rating_of_posts_by_author else rating_of_posts_by_author

        rating_of_comments_by_author = Comment.objects.filter(user=self.user).aggregate(Sum('rating'))['rating__sum']
        rating_of_comments_by_author = 0 if not rating_of_comments_by_author else rating_of_comments_by_author

        rating_of_comments_under_posts_by_author = Comment.objects.filter(post__author__user=self.user).aggregate(Sum('rating'))['rating__sum']
        rating_of_comments_under_posts_by_author = 0 if not rating_of_comments_under_posts_by_author else rating_of_comments_under_posts_by_author

        self.rating = rating_of_posts_by_author + rating_of_comments_by_author + rating_of_comments_under_posts_by_author
        self.save()


class Category(models.Model):
    category_name = models.CharField(max_length=100, unique=True)


class Post(models.Model):
    article = 'AR'
    news = 'NE'

    WRITE_TYPE = [
        (article, 'Статья'),
        (news, 'Новость'),
    ]

    author = models.ForeignKey("Author", on_delete=models.CASCADE, verbose_name='Автор')
    write_type = models.CharField(max_length=2, choices=WRITE_TYPE, default=article, verbose_name='Вид поста')
    time_create = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    time_update = models.DateTimeField(auto_now=True, verbose_name='Дата изменения')
    title = models.CharField(max_length=100, default='default title', verbose_name='Заголовок')
    content = models.CharField(max_length=2500, default='default content', verbose_name='Контент')
    rating = models.IntegerField(default=0)

    category = models.ManyToManyField('Category', through='PostCategory')

    def like(self):
        # post_ = Post.objects.get(pk=self.post_id)
        self.rating += 1
        self.save()

    def dislike(self):
        # post_ = Post.objects.get(pk=self.post_id)
        self.rating -= 1
        self.save()

    def preview(self):
        text = str(self.content)
        return text[:124] + '...'


class PostCategory(models.Model):
    post = models.ForeignKey('Post', on_delete=models.CASCADE)
    category = models.ForeignKey('Category', on_delete=models.CASCADE)


class Comment(models.Model):
    post = models.ForeignKey('Post', on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField(null=True)
    comment_time = models.DateTimeField(auto_now_add=True)
    rating = models.FloatField(default=0.0)

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()
