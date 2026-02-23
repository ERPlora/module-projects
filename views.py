"""
Projects & Time Tracking Module Views
"""
from django.utils.translation import gettext_lazy as _
from django.utils import timezone

from apps.accounts.decorators import login_required
from apps.core.htmx import htmx_view
from apps.modules_runtime.navigation import with_module_nav


@login_required
@with_module_nav('projects', 'dashboard')
@htmx_view('projects/pages/dashboard.html', 'projects/partials/dashboard_content.html')
def dashboard(request):
    """Dashboard view."""
    hub_id = request.session.get('hub_id')
    return {}


@login_required
@with_module_nav('projects', 'projects')
@htmx_view('projects/pages/projects.html', 'projects/partials/projects_content.html')
def projects(request):
    """Projects view."""
    hub_id = request.session.get('hub_id')
    return {}


@login_required
@with_module_nav('projects', 'time')
@htmx_view('projects/pages/time.html', 'projects/partials/time_content.html')
def time(request):
    """Time Entries view."""
    hub_id = request.session.get('hub_id')
    return {}


@login_required
@with_module_nav('projects', 'settings')
@htmx_view('projects/pages/settings.html', 'projects/partials/settings_content.html')
def settings(request):
    """Settings view."""
    hub_id = request.session.get('hub_id')
    return {}

