from django.core.mail import EmailMultiAlternatives
from django.db.models.signals import m2m_changed
from django.dispatch import receiver
from django.template.loader import render_to_string

from news.models import PostCategory
from NewsPaper.settings import SITE_URL, EMAIL_HOST_USER


# def send_notifications(preview, pk, title, subscribers):
#     html_content = render_to_string(
#         'post_created_email.html',
#         {
#             'text': preview,
#             'link': f"{SITE_URL}/news/{pk}"
#         }
#     )
#
#     msg = EmailMultiAlternatives(
#         subject=title,
#         body='',
#         from_email=f'{EMAIL_HOST_USER}@yandex.ru',
#         to=subscribers,
#     )
#
#     msg.attach_alternative(html_content, 'text/html')
#     msg.send()
#
#
# @receiver(m2m_changed, sender=PostCategory)
# def notify_about_new_post(sender, instance, **kwargs):
#     if kwargs['action'] == 'post_add':
#         categories = instance.category.all()
#         subscribers_emails = []
#
#         for cat in categories:
#             subscribers = cat.subscribers.all()
#             subscribers_emails += [s.email for s in subscribers]
#
#         send_notifications(preview=instance.preview, pk=instance.pk, title=instance.title, subscribers=subscribers_emails)
