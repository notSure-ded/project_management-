from celery import shared_task
from django.utils import timezone
from django.core.mail import send_mail
from django.conf import settings
from .models import DevelopmentTask, DesignTask
@shared_task
def mark_overdue_tasks():
    today = timezone.now().date()
    tasks = []
    
    # Check DevelopmentTask
    dev_tasks = DevelopmentTask.objects.filter(
        due_date__lt=today,
        status__in=['todo', 'in_progress']
    )
    print(f"Found {dev_tasks.count()} development tasks to mark as overdue")
    dev_tasks.update(status='overdue')
    tasks.extend(dev_tasks)
    
    # Check DesignTask
    design_tasks = DesignTask.objects.filter(
        due_date__lt=today,
        status__in=['todo', 'in_progress']
    )
    print(f"Found {design_tasks.count()} design tasks to mark as overdue")
    design_tasks.update(status='overdue')
    tasks.extend(design_tasks)
    
    # Send notifications
    for task in tasks:
        print(f"Sending email for task: {task.title}")
        send_mail(
            'Task Overdue Notification',
            f'Task "{task.title}" is overdue!',
            settings.DEFAULT_FROM_EMAIL,
            ['admin@example.com'],
            fail_silently=False,
        )
    
    return f"Marked {len(tasks)} tasks as overdue"