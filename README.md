# Projects & Time Tracking

## Overview

| Property | Value |
|----------|-------|
| **Module ID** | `projects` |
| **Version** | `1.0.0` |
| **Icon** | `git-branch-outline` |
| **Dependencies** | None |

## Models

### `Project`

Project(id, hub_id, created_at, updated_at, created_by, updated_by, is_deleted, deleted_at, name, code, description, status, start_date, end_date, budget, spent)

| Field | Type | Details |
|-------|------|---------|
| `name` | CharField | max_length=255 |
| `code` | CharField | max_length=20, optional |
| `description` | TextField | optional |
| `status` | CharField | max_length=20, choices: active, on_hold, completed, cancelled |
| `start_date` | DateField | optional |
| `end_date` | DateField | optional |
| `budget` | DecimalField |  |
| `spent` | DecimalField |  |

### `TimeEntry`

TimeEntry(id, hub_id, created_at, updated_at, created_by, updated_by, is_deleted, deleted_at, project, employee_id, employee_name, date, hours, description, is_billable)

| Field | Type | Details |
|-------|------|---------|
| `project` | ForeignKey | → `projects.Project`, on_delete=CASCADE |
| `employee_id` | UUIDField | max_length=32 |
| `employee_name` | CharField | max_length=255 |
| `date` | DateField |  |
| `hours` | DecimalField |  |
| `description` | CharField | max_length=255, optional |
| `is_billable` | BooleanField |  |

## Cross-Module Relationships

| From | Field | To | on_delete | Nullable |
|------|-------|----|-----------|----------|
| `TimeEntry` | `project` | `projects.Project` | CASCADE | No |

## URL Endpoints

Base path: `/m/projects/`

| Path | Name | Method |
|------|------|--------|
| `(root)` | `dashboard` | GET |
| `time/` | `time` | GET |
| `projects/` | `projects_list` | GET |
| `projects/add/` | `project_add` | GET/POST |
| `projects/<uuid:pk>/edit/` | `project_edit` | GET |
| `projects/<uuid:pk>/delete/` | `project_delete` | GET/POST |
| `projects/bulk/` | `projects_bulk_action` | GET/POST |
| `settings/` | `settings` | GET |

## Permissions

| Permission | Description |
|------------|-------------|
| `projects.view_project` | View Project |
| `projects.add_project` | Add Project |
| `projects.change_project` | Change Project |
| `projects.delete_project` | Delete Project |
| `projects.view_timeentry` | View Timeentry |
| `projects.add_timeentry` | Add Timeentry |
| `projects.change_timeentry` | Change Timeentry |
| `projects.manage_settings` | Manage Settings |

**Role assignments:**

- **admin**: All permissions
- **manager**: `add_project`, `add_timeentry`, `change_project`, `change_timeentry`, `view_project`, `view_timeentry`
- **employee**: `add_project`, `view_project`, `view_timeentry`

## Navigation

| View | Icon | ID | Fullpage |
|------|------|----|----------|
| Dashboard | `speedometer-outline` | `dashboard` | No |
| Projects | `git-branch-outline` | `projects` | No |
| Time Entries | `time-outline` | `time` | No |
| Settings | `settings-outline` | `settings` | No |

## AI Tools

Tools available for the AI assistant:

### `list_projects`

List projects with optional status filter.

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `status` | string | No | Filter: active, on_hold, completed, cancelled |
| `limit` | integer | No | Max results (default 20) |

### `create_project`

Create a new project.

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `name` | string | Yes | Project name |
| `code` | string | No | Project code |
| `description` | string | No | Project description |
| `budget` | string | No | Budget amount |
| `start_date` | string | No | Start date (YYYY-MM-DD) |
| `end_date` | string | No | End date (YYYY-MM-DD) |

### `log_time_entry`

Log a time entry for a project.

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `project_id` | string | Yes | Project ID |
| `hours` | number | Yes | Hours worked |
| `description` | string | Yes | Work description |
| `date` | string | No | Date (YYYY-MM-DD). Defaults to today. |
| `is_billable` | boolean | No | Billable hours (default true) |

## File Structure

```
README.md
__init__.py
admin.py
ai_tools.py
apps.py
forms.py
locale/
  en/
    LC_MESSAGES/
      django.po
  es/
    LC_MESSAGES/
      django.po
migrations/
  0001_initial.py
  __init__.py
models.py
module.py
static/
  icons/
    icon.svg
  projects/
    css/
    js/
templates/
  projects/
    pages/
      dashboard.html
      index.html
      project_add.html
      project_edit.html
      projects.html
      settings.html
      time.html
    partials/
      dashboard_content.html
      panel_project_add.html
      panel_project_edit.html
      project_add_content.html
      project_edit_content.html
      projects_content.html
      projects_list.html
      settings_content.html
      time_content.html
tests/
  __init__.py
  conftest.py
  test_models.py
  test_views.py
urls.py
views.py
```
