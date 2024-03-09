import logging
import datetime

from django.conf import settings

from django.utils import timezone
from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger
from django.core.management.base import BaseCommand
from django_apscheduler.jobstores import DjangoJobStore
from django_apscheduler.models import DjangoJobExecution
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives, send_mail

from news.models import Post, Category, UserCategory
from django.contrib.auth.models import User
from NewsPaper.settings import SITE_URL, DEFAULT_FROM_EMAIL

logger = logging.getLogger(__name__)


# наша задача по выводу текста на экран
def my_job():
    today = timezone.now()
    last_week = today - datetime.timedelta(days=7)
    posts = Post.objects.filter(time_create__gte=last_week)
    print(posts)

    categories = set(posts.values_list('category__category_name', flat=True))
    subs = set(Category.objects.filter(category_name__in=categories).values_list('usercategory__user', flat=True))
    valid_subs = set(User.objects.filter(id__in=subs).values_list('email', flat=True))
    print(f'categories - {categories}\n, subs - {subs}\n, valid_subs - {valid_subs}')

    for email in valid_subs:
        sub_idx = User.objects.filter(email=email).first().id
        category_lst = list(UserCategory.objects.filter(user=sub_idx).values_list('category', flat=True))
        print(f'category_lst - {category_lst}')

        for ctg in category_lst:
            valid_posts = list(posts.filter(category=ctg))
            print(f'valid_posts - {valid_posts}')

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
    print('Все отправлено')


# функция, которая будет удалять неактуальные задачи
def delete_old_job_executions(max_age=604_800):
    """This job deletes all apscheduler job executions older than `max_age` from the database."""
    DjangoJobExecution.objects.delete_old_job_executions(max_age)


class Command(BaseCommand):
    help = "Runs apscheduler."

    def handle(self, *args, **options):
        scheduler = BlockingScheduler(timezone=settings.TIME_ZONE)
        scheduler.add_jobstore(DjangoJobStore(), "default")

        # добавляем работу нашему задачнику
        scheduler.add_job(
            my_job,
            trigger=CronTrigger(day_of_week="mon", hour="00", minute="00"),
            # То же, что и интервал, но задача тригера таким образом более понятна django
            id="my_job",  # уникальный айди
            max_instances=1,
            replace_existing=True,
        )
        logger.info("Added job 'my_job'.")

        scheduler.add_job(
            delete_old_job_executions,
            trigger=CronTrigger(
                day_of_week="mon", hour="00", minute="00"
            ),
            # Каждую неделю будут удаляться старые задачи, которые либо не удалось выполнить, либо уже выполнять не надо.
            id="delete_old_job_executions",
            max_instances=1,
            replace_existing=True,
        )
        logger.info(
            "Added weekly job: 'delete_old_job_executions'."
        )

        try:
            logger.info("Starting scheduler...")
            scheduler.start()
        except KeyboardInterrupt:
            logger.info("Stopping scheduler...")
            scheduler.shutdown()
            logger.info("Scheduler shut down successfully!")