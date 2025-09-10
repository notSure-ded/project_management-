from django.test import TestCase, TransactionTestCase
from django.utils import timezone
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from rest_framework import status
from core.models import Project, DevelopmentTask, DesignTask
from datetime import timedelta
from django.core import mail
from django.db import connection

class ProjectModelTest(TestCase):
    def setUp(self):
        self.project = Project.objects.create(
            name="Test Project",
            start_date=timezone.now().date(),
            end_date=timezone.now().date() + timedelta(days=10)
        )

    def test_project_creation(self):
        self.assertEqual(self.project.name, "Test Project")
        self.assertEqual(self.project.start_date, timezone.now().date())
        self.assertEqual(self.project.end_date, timezone.now().date() + timedelta(days=10))

class DevelopmentTaskModelTest(TestCase):
    def setUp(self):
        self.project = Project.objects.create(
            name="Test Project",
            start_date=timezone.now().date(),
            end_date=timezone.now().date() + timedelta(days=10)
        )
        self.task = DevelopmentTask.objects.create(
            title="Dev Task",
            due_date=timezone.now().date() + timedelta(days=5),
            project=self.project,
            language="Python"
        )

    def test_task_creation(self):
        self.assertEqual(self.task.title, "Dev Task")
        self.assertEqual(self.task.language, "Python")
        self.assertEqual(self.task.project, self.project)

class ProjectAPITest(TransactionTestCase):
    def setUp(self):
        # Clear all data
        User.objects.all().delete()
        Project.objects.all().delete()
        DevelopmentTask.objects.all().delete()
        DesignTask.objects.all().delete()
        
        # Create a user and authenticate
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)
        
        # Create a test project
        self.project = Project.objects.create(
            name="Test Project",
            start_date=timezone.now().date(),
            end_date=timezone.now().date() + timedelta(days=10)
        )

    def test_get_projects(self):
        url = '/api/projects/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_create_project(self):
        url = '/api/projects/'
        data = {
            'name': 'New Project',
            'start_date': timezone.now().date().isoformat(),
            'end_date': (timezone.now().date() + timedelta(days=20)).isoformat()
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

class DevelopmentTaskAPITest(TransactionTestCase):
    def setUp(self):
        # Clear all data
        User.objects.all().delete()
        Project.objects.all().delete()
        DevelopmentTask.objects.all().delete()
        DesignTask.objects.all().delete()
        
        # Create a user and authenticate
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)
        
        # Create a test project
        self.project = Project.objects.create(
            name="Test Project",
            start_date=timezone.now().date(),
            end_date=timezone.now().date() + timedelta(days=10)
        )
        
        # Create a test task
        self.task = DevelopmentTask.objects.create(
            title="Dev Task",
            due_date=timezone.now().date() + timedelta(days=5),
            project=self.project,
            language="Python"
        )

    def test_get_tasks(self):
        url = '/api/development-tasks/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_filter_tasks_by_status(self):
        url = '/api/development-tasks/?status=todo'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

class SignalTest(TestCase):
    def test_task_creation_signal(self):
        # Use the test mail backend
        with self.settings(EMAIL_BACKEND='django.core.mail.backends.locmem.EmailBackend'):
            # Clear the mail outbox
            mail.outbox = []
            
            project = Project.objects.create(
                name="Test Project",
                start_date=timezone.now().date(),
                end_date=timezone.now().date() + timedelta(days=10)
            )
            DevelopmentTask.objects.create(
                title="Dev Task",
                due_date=timezone.now().date() + timedelta(days=5),
                project=project,
                language="Python"
            )
            # Check that one message has been sent
            self.assertEqual(len(mail.outbox), 1)
            # Verify the subject
            self.assertEqual(mail.outbox[0].subject, 'New Task Created')

class CeleryTaskTest(TestCase):
    def test_mark_overdue_tasks(self):
        # Use the test mail backend
        with self.settings(EMAIL_BACKEND='django.core.mail.backends.locmem.EmailBackend'):
            # Clear the mail outbox
            mail.outbox = []
            
            project = Project.objects.create(
                name="Test Project",
                start_date=timezone.now().date() - timedelta(days=5),
                end_date=timezone.now().date() + timedelta(days=5)
            )
            task = DevelopmentTask.objects.create(
                title="Overdue Task",
                due_date=timezone.now().date() - timedelta(days=1),
                project=project,
                language="Python",
                status="todo"
            )
            
            # Clear the mail outbox again after the task creation signal
            mail.outbox = []
            
            from core.tasks import mark_overdue_tasks
            mark_overdue_tasks()
            
            task.refresh_from_db()
            self.assertEqual(task.status, 'overdue')
            
            # Check that one message has been sent
            self.assertEqual(len(mail.outbox), 1)
            # Verify the subject
            self.assertEqual(mail.outbox[0].subject, 'Task Overdue Notification')