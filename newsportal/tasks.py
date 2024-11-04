from celery import shared_task
from datetime import timedelta
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from .models import Post, PostCategory
from django.contrib.auth.models import User
from django.utils import timezone

@shared_task
def send_new_post_notification(post_id):
    '''метод для отправки уведомление о создание нового поста'''
    global subject
    try:
        # получаем данные поста
        post = Post.objects.get(id=post_id)
        # все категории данного поста
        categories = post.category.all()
        # получаем наименование категорий для темы письма
        category = PostCategory.objects.filter(post=post)

        for cat in category:
            subject = f'Новый пост в категории {cat.name}'


        # Генерируем текстовое и HTML-содержание
        text_content = f'Новый пост: {post.title}\n\nСсылка: http://127.0.0.1:8000{post.get_absolute_url()}'
        html_content = (f'Новый пост: {post.title}<br>'f'<a href="http://127.0.0.1:8000{post.get_absolute_url()}">'f'Ссылка на пост</a>')

        for category in categories:
            # сбор всех подписчиков данной категории
            subscribers = category.subscriptions.all()
            for sub in subscribers:
                email = EmailMultiAlternatives(
                    subject=subject,
                    body=text_content,
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    to=[sub.user.email],)
                email.attach_alternative(html_content, "text/html")
                email.send()
    except Post.DoesNotExist:
        # Логика обработки, если пост не найден (например, удалить задачу)
        pass

@shared_task
def weekly_send_posts():
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