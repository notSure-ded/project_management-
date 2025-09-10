from rest_framework import viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend
from .models import Project, DevelopmentTask, DesignTask
from .serializers import ProjectSerializer, DevelopmentTaskSerializer, DesignTaskSerializer

class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['start_date', 'end_date']
    search_fields = ['name', 'description']
    ordering_fields = ['name', 'start_date', 'end_date']

class TaskViewSetMixin:
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['status', 'due_date', 'project']
    search_fields = ['title', 'description']
    ordering_fields = ['title', 'due_date', 'status']

class DevelopmentTaskViewSet(TaskViewSetMixin, viewsets.ModelViewSet):
    queryset = DevelopmentTask.objects.all()
    serializer_class = DevelopmentTaskSerializer

class DesignTaskViewSet(TaskViewSetMixin, viewsets.ModelViewSet):
    queryset = DesignTask.objects.all()
    serializer_class = DesignTaskSerializer