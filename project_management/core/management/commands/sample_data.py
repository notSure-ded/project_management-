from django.core.management.base import BaseCommand
from django.utils import timezone
from core.models import Project, DevelopmentTask, DesignTask
from datetime import timedelta
from django.conf import settings

class Command(BaseCommand):
    help = 'Load sample data for testing'
    
    def handle(self, *args, **kwargs):
        # Don't load sample data in test environment
        if settings.DEBUG:
            # Create project
            project = Project.objects.create(
                name="Sample Project",
                description="This is a sample project",
                start_date=timezone.now().date(),
                end_date=timezone.now().date() + timedelta(days=30)
            )
            
            # Create tasks
            DevelopmentTask.objects.create(
                title="Setup Development Environment",
                due_date=timezone.now().date() + timedelta(days=7),
                project=project,
                language="Python",
                framework="Django"
            )
            
            DesignTask.objects.create(
                title="Create Mockups",
                due_date=timezone.now().date() + timedelta(days=10),
                project=project,
                tool="Figma",
                file_format="png"
            )
            
            self.stdout.write(self.style.SUCCESS('Sample data loaded successfully.'))
        else:
            self.stdout.write(self.style.WARNING('Not loading sample data in production environment.'))