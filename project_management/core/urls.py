from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ProjectViewSet, DevelopmentTaskViewSet, DesignTaskViewSet

router = DefaultRouter()
router.register(r'projects', ProjectViewSet)
router.register(r'development-tasks', DevelopmentTaskViewSet)
router.register(r'design-tasks', DesignTaskViewSet)

urlpatterns = [
    path('', include(router.urls)),
]