from django.urls import path
from . import views

app_name = 'projects'

urlpatterns = [
    # Dashboard
    path('', views.dashboard, name='dashboard'),

    # Project
    path('projects/', views.projects_list, name='projects_list'),
    path('projects/add/', views.project_add, name='project_add'),
    path('projects/<uuid:pk>/edit/', views.project_edit, name='project_edit'),
    path('projects/<uuid:pk>/delete/', views.project_delete, name='project_delete'),
    path('projects/bulk/', views.projects_bulk_action, name='projects_bulk_action'),

    # Settings
    path('settings/', views.settings_view, name='settings'),
]
