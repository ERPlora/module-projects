from django.urls import path
from . import views

app_name = 'projects'

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('projects/', views.projects, name='projects'),
    path('time/', views.time, name='time'),
    path('settings/', views.settings, name='settings'),
]
