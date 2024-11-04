import logging
from django.contrib.auth.models import User
from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger
from django.conf import settings
from django.core.mail import send_mail, mail_managers
from django.core.management.base import BaseCommand
from django_apscheduler import util
from django_apscheduler.jobstores import DjangoJobStore
from django_apscheduler.models import DjangoJobExecution
from datetime import timedelta
from django.utils import timezone

from django.core.mail import EmailMultiAlternatives

from NP.newsportal.models import Post

logger = logging.getLogger(__name__)


def send_week_posts():
    # Текущее время
    now_time = timezone.now()
    # Дата 7 дней назад
    week_ago = now_time - timedelta(days=7)

    # Отфильтрованный queryset с постами за последние 7 дней
    recent_posts = Post.objects.filter(date__range=(week_ago, now_time)).prefetch_related('category')

    # Проходим по всем постам
    for post in recent_posts:
        # Получаем список адресов электронной почты подписчиков на категории поста
        emails = User.objects.filter(
            subscriptions__category__in=post.category.all()
        ).values_list('email', flat=True)
        # Преобразуем QuerySet в список
        email_list = list(emails)

        subject = 'Еженедельная рассылка постов AnimeNews'
        text_content = (
            f'Пост: {post.title}\n'
            f'Ссылка на пост: http://127.0.0.1:8000{post.get_absolute_url()}'
        )
        html_content = (
            f'Пост: {post.title}<br>'
            f'<a href="http://127.0.0.1:8000{post.get_absolute_url()}">'
            f'Ссылка на пост</a>'
        )
        # Отправка писем всем подписчикам
        for email in email_list:
            msg = EmailMultiAlternatives(subject, text_content, None, [email])
            msg.attach_alternative(html_content, "text/html")
            msg.send()



@util.close_old_connections
def delete_old_job_executions(max_age=604_800):
    DjangoJobExecution.objects.delete_old_job_executions(max_age)


class Command(BaseCommand):
    help = "Runs APScheduler."

    def handle(self, *args, **options):
        scheduler = BlockingScheduler(timezone=settings.TIME_ZONE)
        scheduler.add_jobstore(DjangoJobStore(), "default")

        scheduler.add_job(
            send_week_posts,
            trigger=CronTrigger(day_of_week="fri", hour="18", minute="00"),
            id="send_week_posts",  # The `id` assigned to each job MUST be unique
            max_instances=1,
            replace_existing=True,
        )
        logger.info("Added posts 'send_week_posts'.")

        scheduler.add_job(
            delete_old_job_executions,
            trigger=CronTrigger(
                day_of_week="mon", hour="00", minute="00"
            ),
            id="delete_old_job_executions",
            max_instances=1,
            replace_existing=True,
        )
        logger.info("Added weekly job: 'delete_old_job_executions'.")

        try:
            logger.info("Starting scheduler...")
            scheduler.start()
        except KeyboardInterrupt:
            logger.info("Stopping scheduler...")
            scheduler.shutdown()
            logger.info("Scheduler shut down successfully!")