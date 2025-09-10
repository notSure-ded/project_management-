from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from django.conf import settings
from .models import DevelopmentTask, DesignTask

@receiver(post_save, sender=DevelopmentTask)
@receiver(post_save, sender=DesignTask)
def notify_task_creation(sender, instance, created, **kwargs):
    if created:
        send_mail(
            'New Task Created',
            f'Task "{instance.title}" was created in project "{instance.project.name}"',
            settings.DEFAULT_FROM_EMAIL,
            ['admin@example.com'],
            fail_silently=False,
        )