from datetime import datetime, timedelta

from django.core.mail import mail_managers
from django.utils import timezone
from django.conf.global_settings import EMAIL_HOST_USER
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.conf import settings
from celery import shared_task

from news.models import Post, Category, UserCategory
from django.contrib.auth.models import User
from NewsPaper.settings import SITE_URL, DEFAULT_FROM_EMAIL


# def send_mails():
#     print('Hello from background task!')
#
#
# @shared_task
# def hello():
#     time.sleep(10)
#     print("Hello, world!")
#
#
# @shared_task
# def printer(N):
#     for i in range(N):
#         time.sleep(1)
#         print(i+1)

@shared_task
def new_post(pk):
    post = Post.objects.get(pk=pk)
    categories = post.category.all()
    title = post.title
    preview = post.preview()
    subs = categories.values_list('usercategory__user', flat=True)
    subscribers_emails = set(User.objects.filter(id__in=subs).values_list('email', flat=True))

    html_content = render_to_string(
        'post_created_email.html',
        {
            'text': preview,
            'link': f'{settings.SITE_URL}/news/{pk}'
        }
    )

    msg = EmailMultiAlternatives(
        subject=title,
        body='',
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=subscribers_emails,
    )

    msg.attach_alternative(html_content, 'text/html')
    msg.send()


@shared_task
def weekly_post():
    today = timezone.now()
    last_week = today - datetime.timedelta(days=7)
    posts = Post.objects.filter(time_create__gte=last_week)
    categories = set(posts.values_list('category__category_name', flat=True))
    subs = set(Category.objects.filter(category_name__in=categories).values_list('usercategory__user', flat=True))
    valid_subs = set(User.objects.filter(id__in=subs).values_list('email', flat=True))

    for email in valid_subs:
        html_content = render_to_string(
            'post_week.html',
            {
                'link': SITE_URL,
                'posts': posts,

            }
        )

        msg = EmailMultiAlternatives(
            subject='Новости за неделю',
            body='',
            from_email=DEFAULT_FROM_EMAIL,
            to=[email],
        )
        msg.attach_alternative(html_content, 'text/html')
        msg.send()
