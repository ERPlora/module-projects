"""AI tools for the Projects module."""
from assistant.tools import AssistantTool, register_tool


@register_tool
class ListProjects(AssistantTool):
    name = "list_projects"
    description = "List projects with optional status filter."
    module_id = "projects"
    required_permission = "projects.view_project"
    parameters = {
        "type": "object",
        "properties": {
            "status": {"type": "string", "description": "Filter: active, on_hold, completed, cancelled"},
            "limit": {"type": "integer", "description": "Max results (default 20)"},
        },
        "required": [],
        "additionalProperties": False,
    }

    def execute(self, args, request):
        from projects.models import Project
        qs = Project.objects.all().order_by('-start_date')
        if args.get('status'):
            qs = qs.filter(status=args['status'])
        limit = args.get('limit', 20)
        return {
            "projects": [
                {
                    "id": str(p.id),
                    "name": p.name,
                    "code": p.code,
                    "status": p.status,
                    "budget": str(p.budget) if p.budget else None,
                    "spent": str(p.spent) if p.spent else None,
                    "start_date": str(p.start_date) if p.start_date else None,
                    "end_date": str(p.end_date) if p.end_date else None,
                }
                for p in qs[:limit]
            ],
            "total": qs.count(),
        }


@register_tool
class CreateProject(AssistantTool):
    name = "create_project"
    description = "Create a new project."
    module_id = "projects"
    required_permission = "projects.change_project"
    requires_confirmation = True
    parameters = {
        "type": "object",
        "properties": {
            "name": {"type": "string", "description": "Project name"},
            "code": {"type": "string", "description": "Project code"},
            "description": {"type": "string", "description": "Project description"},
            "budget": {"type": "string", "description": "Budget amount"},
            "start_date": {"type": "string", "description": "Start date (YYYY-MM-DD)"},
            "end_date": {"type": "string", "description": "End date (YYYY-MM-DD)"},
        },
        "required": ["name"],
        "additionalProperties": False,
    }

    def execute(self, args, request):
        from decimal import Decimal
        from projects.models import Project
        p = Project.objects.create(
            name=args['name'],
            code=args.get('code', ''),
            description=args.get('description', ''),
            budget=Decimal(args['budget']) if args.get('budget') else None,
            start_date=args.get('start_date'),
            end_date=args.get('end_date'),
            status='active',
        )
        return {"id": str(p.id), "name": p.name, "code": p.code, "created": True}


@register_tool
class LogTimeEntry(AssistantTool):
    name = "log_time_entry"
    description = "Log a time entry for a project."
    module_id = "projects"
    required_permission = "projects.change_project"
    requires_confirmation = True
    parameters = {
        "type": "object",
        "properties": {
            "project_id": {"type": "string", "description": "Project ID"},
            "hours": {"type": "number", "description": "Hours worked"},
            "description": {"type": "string", "description": "Work description"},
            "date": {"type": "string", "description": "Date (YYYY-MM-DD). Defaults to today."},
            "is_billable": {"type": "boolean", "description": "Billable hours (default true)"},
        },
        "required": ["project_id", "hours", "description"],
        "additionalProperties": False,
    }

    def execute(self, args, request):
        from datetime import date
        from projects.models import TimeEntry
        user_id = request.session.get('local_user_id')
        from apps.accounts.models import LocalUser
        user = LocalUser.objects.get(id=user_id)
        te = TimeEntry.objects.create(
            project_id=args['project_id'],
            employee_id=user_id,
            employee_name=user.name,
            hours=args['hours'],
            description=args['description'],
            date=args.get('date', date.today()),
            is_billable=args.get('is_billable', True),
        )
        return {"id": str(te.id), "hours": te.hours, "created": True}


@register_tool
class UpdateProject(AssistantTool):
    name = "update_project"
    description = "Update a project's fields."
    module_id = "projects"
    required_permission = "projects.change_project"
    requires_confirmation = True
    parameters = {
        "type": "object",
        "properties": {
            "project_id": {"type": "string"},
            "name": {"type": "string"},
            "code": {"type": "string"},
            "description": {"type": "string"},
            "status": {"type": "string", "description": "active, on_hold, completed, cancelled"},
            "start_date": {"type": "string"},
            "end_date": {"type": "string"},
            "budget": {"type": "string"},
        },
        "required": ["project_id"],
        "additionalProperties": False,
    }

    def execute(self, args, request):
        from decimal import Decimal
        from projects.models import Project
        try:
            p = Project.objects.get(id=args['project_id'])
        except Project.DoesNotExist:
            return {"error": "Project not found"}
        fields = []
        for field in ('name', 'code', 'description', 'status', 'start_date', 'end_date'):
            if field in args:
                setattr(p, field, args[field])
                fields.append(field)
        if 'budget' in args:
            p.budget = Decimal(args['budget'])
            fields.append('budget')
        if fields:
            p.save(update_fields=fields + ['updated_at'])
        return {"id": str(p.id), "name": p.name, "updated": True}


@register_tool
class DeleteProject(AssistantTool):
    name = "delete_project"
    description = "Delete a project."
    module_id = "projects"
    required_permission = "projects.delete_project"
    requires_confirmation = True
    parameters = {
        "type": "object",
        "properties": {"project_id": {"type": "string"}},
        "required": ["project_id"],
        "additionalProperties": False,
    }

    def execute(self, args, request):
        from projects.models import Project
        try:
            p = Project.objects.get(id=args['project_id'])
            name = p.name
            p.delete()
            return {"deleted": True, "name": name}
        except Project.DoesNotExist:
            return {"error": "Project not found"}


@register_tool
class UpdateProjectTask(AssistantTool):
    name = "update_project_task"
    description = "Update a project time entry (description, hours, date, billable flag)."
    module_id = "projects"
    required_permission = "projects.change_project"
    requires_confirmation = True
    parameters = {
        "type": "object",
        "properties": {
            "entry_id": {"type": "string"},
            "description": {"type": "string"},
            "hours": {"type": "number"},
            "date": {"type": "string"},
            "is_billable": {"type": "boolean"},
        },
        "required": ["entry_id"],
        "additionalProperties": False,
    }

    def execute(self, args, request):
        from projects.models import TimeEntry
        try:
            te = TimeEntry.objects.get(id=args['entry_id'])
        except TimeEntry.DoesNotExist:
            return {"error": "Time entry not found"}
        fields = []
        for field in ('description', 'hours', 'date', 'is_billable'):
            if field in args:
                setattr(te, field, args[field])
                fields.append(field)
        if fields:
            te.save(update_fields=fields + ['updated_at'])
        return {"id": str(te.id), "updated": True}


@register_tool
class DeleteProjectTask(AssistantTool):
    name = "delete_project_task"
    description = "Delete a project time entry."
    module_id = "projects"
    required_permission = "projects.change_project"
    requires_confirmation = True
    parameters = {
        "type": "object",
        "properties": {"entry_id": {"type": "string"}},
        "required": ["entry_id"],
        "additionalProperties": False,
    }

    def execute(self, args, request):
        from projects.models import TimeEntry
        try:
            te = TimeEntry.objects.get(id=args['entry_id'])
            te.delete()
            return {"deleted": True}
        except TimeEntry.DoesNotExist:
            return {"error": "Time entry not found"}
