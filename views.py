"""
Projects & Time Tracking Module Views
"""
from django.core.paginator import Paginator
from django.db.models import Q, Count
from django.shortcuts import get_object_or_404, render as django_render
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.views.decorators.http import require_POST

from apps.accounts.decorators import login_required, permission_required
from apps.core.htmx import htmx_view
from apps.core.services import export_to_csv, export_to_excel
from apps.modules_runtime.navigation import with_module_nav

from .models import Project, TimeEntry

PER_PAGE_CHOICES = [10, 25, 50, 100]


# ======================================================================
# Dashboard
# ======================================================================

@login_required
@with_module_nav('projects', 'dashboard')
@htmx_view('projects/pages/index.html', 'projects/partials/dashboard_content.html')
def dashboard(request):
    hub_id = request.session.get('hub_id')
    return {
        'total_projects': Project.objects.filter(hub_id=hub_id, is_deleted=False).count(),
    }


# ======================================================================
# Project
# ======================================================================

PROJECT_SORT_FIELDS = {
    'code': 'code',
    'name': 'name',
    'status': 'status',
    'spent': 'spent',
    'budget': 'budget',
    'description': 'description',
    'created_at': 'created_at',
}

def _build_projects_context(hub_id, per_page=10):
    qs = Project.objects.filter(hub_id=hub_id, is_deleted=False).order_by('code')
    paginator = Paginator(qs, per_page)
    page_obj = paginator.get_page(1)
    return {
        'projects': page_obj,
        'page_obj': page_obj,
        'search_query': '',
        'sort_field': 'code',
        'sort_dir': 'asc',
        'current_view': 'table',
        'per_page': per_page,
    }

def _render_projects_list(request, hub_id, per_page=10):
    ctx = _build_projects_context(hub_id, per_page)
    return django_render(request, 'projects/partials/projects_list.html', ctx)

@login_required
@with_module_nav('projects', 'projects')
@htmx_view('projects/pages/projects.html', 'projects/partials/projects_content.html')
def projects_list(request):
    hub_id = request.session.get('hub_id')
    search_query = request.GET.get('q', '').strip()
    sort_field = request.GET.get('sort', 'code')
    sort_dir = request.GET.get('dir', 'asc')
    page_number = request.GET.get('page', 1)
    current_view = request.GET.get('view', 'table')
    per_page = int(request.GET.get('per_page', 10))
    if per_page not in PER_PAGE_CHOICES:
        per_page = 10

    qs = Project.objects.filter(hub_id=hub_id, is_deleted=False)

    if search_query:
        qs = qs.filter(Q(name__icontains=search_query) | Q(code__icontains=search_query) | Q(description__icontains=search_query) | Q(status__icontains=search_query))

    order_by = PROJECT_SORT_FIELDS.get(sort_field, 'code')
    if sort_dir == 'desc':
        order_by = f'-{order_by}'
    qs = qs.order_by(order_by)

    export_format = request.GET.get('export')
    if export_format in ('csv', 'excel'):
        fields = ['code', 'name', 'status', 'spent', 'budget', 'description']
        headers = ['Code', 'Name', 'Status', 'Spent', 'Budget', 'Description']
        if export_format == 'csv':
            return export_to_csv(qs, fields=fields, headers=headers, filename='projects.csv')
        return export_to_excel(qs, fields=fields, headers=headers, filename='projects.xlsx')

    paginator = Paginator(qs, per_page)
    page_obj = paginator.get_page(page_number)

    if request.htmx and request.htmx.target == 'datatable-body':
        return django_render(request, 'projects/partials/projects_list.html', {
            'projects': page_obj, 'page_obj': page_obj,
            'search_query': search_query, 'sort_field': sort_field,
            'sort_dir': sort_dir, 'current_view': current_view, 'per_page': per_page,
        })

    return {
        'projects': page_obj, 'page_obj': page_obj,
        'search_query': search_query, 'sort_field': sort_field,
        'sort_dir': sort_dir, 'current_view': current_view, 'per_page': per_page,
    }

@login_required
def project_add(request):
    hub_id = request.session.get('hub_id')
    if request.method == 'POST':
        name = request.POST.get('name', '').strip()
        code = request.POST.get('code', '').strip()
        description = request.POST.get('description', '').strip()
        status = request.POST.get('status', '').strip()
        start_date = request.POST.get('start_date') or None
        end_date = request.POST.get('end_date') or None
        budget = request.POST.get('budget', '0') or '0'
        spent = request.POST.get('spent', '0') or '0'
        obj = Project(hub_id=hub_id)
        obj.name = name
        obj.code = code
        obj.description = description
        obj.status = status
        obj.start_date = start_date
        obj.end_date = end_date
        obj.budget = budget
        obj.spent = spent
        obj.save()
        return _render_projects_list(request, hub_id)
    return django_render(request, 'projects/partials/panel_project_add.html', {})

@login_required
def project_edit(request, pk):
    hub_id = request.session.get('hub_id')
    obj = get_object_or_404(Project, pk=pk, hub_id=hub_id, is_deleted=False)
    if request.method == 'POST':
        obj.name = request.POST.get('name', '').strip()
        obj.code = request.POST.get('code', '').strip()
        obj.description = request.POST.get('description', '').strip()
        obj.status = request.POST.get('status', '').strip()
        obj.start_date = request.POST.get('start_date') or None
        obj.end_date = request.POST.get('end_date') or None
        obj.budget = request.POST.get('budget', '0') or '0'
        obj.spent = request.POST.get('spent', '0') or '0'
        obj.save()
        return _render_projects_list(request, hub_id)
    return django_render(request, 'projects/partials/panel_project_edit.html', {'obj': obj})

@login_required
@require_POST
def project_delete(request, pk):
    hub_id = request.session.get('hub_id')
    obj = get_object_or_404(Project, pk=pk, hub_id=hub_id, is_deleted=False)
    obj.is_deleted = True
    obj.deleted_at = timezone.now()
    obj.save(update_fields=['is_deleted', 'deleted_at', 'updated_at'])
    return _render_projects_list(request, hub_id)

@login_required
@require_POST
def projects_bulk_action(request):
    hub_id = request.session.get('hub_id')
    ids = [i.strip() for i in request.POST.get('ids', '').split(',') if i.strip()]
    action = request.POST.get('action', '')
    qs = Project.objects.filter(hub_id=hub_id, is_deleted=False, id__in=ids)
    if action == 'delete':
        qs.update(is_deleted=True, deleted_at=timezone.now())
    return _render_projects_list(request, hub_id)


@login_required
@permission_required('projects.manage_settings')
@with_module_nav('projects', 'settings')
@htmx_view('projects/pages/settings.html', 'projects/partials/settings_content.html')
def settings_view(request):
    return {}

