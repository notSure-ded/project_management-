from django.contrib import admin
from .models import Project, DevelopmentTask, DesignTask

class DevelopmentTaskInline(admin.TabularInline):
    model = DevelopmentTask
    extra = 0

class DesignTaskInline(admin.TabularInline):
    model = DesignTask
    extra = 0

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'start_date', 'end_date')
    search_fields = ('name', 'description')
    list_filter = ('start_date', 'end_date')
    inlines = [DevelopmentTaskInline, DesignTaskInline]

@admin.register(DevelopmentTask)
class DevelopmentTaskAdmin(admin.ModelAdmin):
    list_display = ('title', 'project', 'due_date', 'status', 'language')
    search_fields = ('title', 'description')
    list_filter = ('status', 'due_date', 'project')

@admin.register(DesignTask)
class DesignTaskAdmin(admin.ModelAdmin):
    list_display = ('title', 'project', 'due_date', 'status', 'tool')
    search_fields = ('title', 'description')
    list_filter = ('status', 'due_date', 'project')