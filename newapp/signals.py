from django.db.models.signals import post_save, m2m_changed
from django.dispatch import receiver
from .models import Post
from django.core.mail import mail_managers

@receiver(post_save, sender = Post)
def notify_subscribers(sender,instance,created, **kwargs):
    if created:
        news_out_category(instance)