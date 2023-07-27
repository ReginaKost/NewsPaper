from django.core.mail import EmailMultiAlternatives
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.template.loader import render_to_string

from .models import Post, Category

@receiver(post_save, sender=Post)
def notify_users_post(sender, instance, created, **kwargs):
    post = Post.objects.get(id=instance.id)
    for cat in post.postCategory.all():
        category_for_subsc_users = Category.objects.get(id=cat.id)
        for user in category_for_subsc_users.subscribers.all():
            html_content = render_to_string(
                'post_dispatch.html',
                {
                    'post': instance,
                    'user_name': user.username,
                }
            )
            msg = EmailMultiAlternatives(
                subject=instance.header,
                from_email='rksendler@gmail.com',
                to=[str(user.email)]
            )
            msg.attach_alternative(html_content, "text/html")
            msg.send()