from django.db import models
from django.utils import timezone
class TimeStampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
        ordering = ['-created_at']  

class Project(TimeStampedModel):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    start_date = models.DateField(default=timezone.now)
    end_date = models.DateField()
    
    class Meta:
        ordering = ['name'] 
    
    def __str__(self):
        return self.name

class Task(TimeStampedModel):
    STATUS_CHOICES = [
        ('todo', 'To Do'),
        ('in_progress', 'In Progress'),
        ('done', 'Done'),
        ('overdue', 'Overdue'),
    ]
    
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    due_date = models.DateField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='todo')
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='+')

    class Meta:
        abstract = True
        ordering = ['due_date']  

    def __str__(self):
        return self.title

class DevelopmentTask(Task):
    language = models.CharField(max_length=50)
    framework = models.CharField(max_length=50, blank=True)
    
    class Meta:
        ordering = ['due_date'] 

class DesignTask(Task):
    tool = models.CharField(max_length=50)
    file_format = models.CharField(max_length=10, blank=True)
    
    class Meta:
        ordering = ['due_date']  