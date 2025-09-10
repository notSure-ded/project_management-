from rest_framework import serializers
from .models import Project, DevelopmentTask, DesignTask

class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = '__all__'

class DevelopmentTaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = DevelopmentTask
        fields = '__all__'

class DesignTaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = DesignTask
        fields = '__all__'