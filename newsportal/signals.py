from django.contrib.auth.models import User
from django.core.mail import EmailMultiAlternatives
from django.db.models.signals import m2m_changed
from django.dispatch import receiver

from .models import PostCategory


@receiver(m2m_changed, sender=PostCategory)
def product_created(instance, **kwargs):
    if not kwargs['action'] == 'post_add':
        return

    emails = User.objects.filter(
        subscriptions__category__in=instance.category.all()
    ).values_list('email', flat=True)

    subject = f'Новый пост в категории {instance.category.name}'

    text_content = (
        f'Пост: {instance.title}\n'
        f'Ссылка на пост: http://127.0.0.1:8000{instance.get_absolute_url()}'
    )
    html_content = (
        f'Пост: {instance.title}<br>'
        f'<a href="http://127.0.0.1{instance.get_absolute_url()}">'
        f'Ссылка на пост</a>'
    )
    for email in emails:
        msg = EmailMultiAlternatives(subject, text_content, None, [email])
        msg.attach_alternative(html_content, "text/html")
        msg.send()