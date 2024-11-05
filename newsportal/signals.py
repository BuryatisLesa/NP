# from django.contrib.auth.models import User
# from django.core.mail import EmailMultiAlternatives
from django.db.models.signals import post_save
from django.dispatch import receiver
from .tasks import send_new_post_notification
from .models import Post


# @receiver(m2m_changed, sender=PostCategory)
# def product_created(instance, **kwargs):
#     if not kwargs['action'] == 'post_add':
#         return
#
#     emails = User.objects.filter(
#         subscriptions__category__in=instance.category.all()
#     ).values_list('email', flat=True)
#
#     subject = f'Новый пост в категории {instance.category.name}'
#
#     text_content = (
#         f'Пост: {instance.title}\n'
#         f'Ссылка на пост: http://127.0.0.1:8000{instance.get_absolute_url()}'
#     )
#     html_content = (
#         f'Пост: {instance.title}<br>'
#         f'<a href="http://127.0.0.1{instance.get_absolute_url()}">'
#         f'Ссылка на пост</a>'
#     )
#     for email in emails:
#         msg = EmailMultiAlternatives(subject, text_content, None, [email])
#         msg.attach_alternative(html_content, "text/html")
#         msg.send()

@receiver(post_save, sender=Post)
def notify_subscribers_on_new_post(sender, instance, created, **kwargs):
    if created:  # Проверяем, что пост был только что создан
        send_new_post_notification.delay(instance.id)
