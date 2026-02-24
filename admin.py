from django.contrib import admin

from .models import Project, TimeEntry

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ['name', 'code', 'status', 'start_date', 'created_at']
    search_fields = ['name', 'code', 'description', 'status']
    readonly_fields = ['created_at', 'updated_at']

@admin.register(TimeEntry)
class TimeEntryAdmin(admin.ModelAdmin):
    list_display = ['project', 'employee_id', 'employee_name', 'date', 'hours', 'created_at']
    search_fields = ['employee_name', 'description']
    readonly_fields = ['created_at', 'updated_at']

