from django.core.mail import EmailMultiAlternatives
from django.db.models.signals import m2m_changed
from django.dispatch import receiver
from django.template.loader import render_to_string

from news.models import PostCategory
from NewsPaper.settings import SITE_URL, EMAIL_HOST_USER
from .models import UserCategory
from django.contrib.auth.models import User


def send_notifications(preview, pk, title, subscribers):
    html_content = render_to_string(
        'post_created_email.html',
        {
            'text': preview,
            'link': f"{SITE_URL}/news/{pk}"
        }
    )

    msg = EmailMultiAlternatives(
        subject=title,
        body='',
        from_email=f'{EMAIL_HOST_USER}@yandex.ru',
        to=subscribers,
    )

    # msg.attach_alternative(html_content, 'text/html')
    # msg.send()


@receiver(m2m_changed, sender=PostCategory)
def notify_about_new_post(sender, instance, **kwargs):
    if kwargs['action'] == 'post_add':
        categories = instance.category.all()
        print(f'categories - {categories}')
        subscribers_emails = []

        for cat in categories:
            subscribers = list(UserCategory.objects.filter(category=cat).values_list('user_id', flat=True))
            subscribers_emails = [User.objects.filter(id=s).values_list('email', flat=True) for s in subscribers]
            print(f'subscribers = {subscribers}, emails = {subscribers_emails}')
            # subscribers = cat.subscribers.all()
            # subscribers_emails += [s.email for s in subscribers]
        print(f'subscribers_emails - {subscribers_emails}')

        send_notifications(preview=instance.preview, pk=instance.pk, title=instance.title, subscribers=subscribers_emails)


