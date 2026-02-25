# Projects & Time Tracking Module

Project management, milestones and time tracking.

## Features

- Project creation with code, description, and date range
- Project status workflow: active, on hold, completed, cancelled
- Budget tracking with allocated budget and spent amount
- Time entry logging per project with employee reference
- Billable and non-billable hour classification
- Per-entry descriptions for detailed work logging
- Date-based time tracking for reporting

## Installation

This module is installed automatically via the ERPlora Marketplace.

## Configuration

Access settings via: **Menu > Projects & Time Tracking > Settings**

## Usage

Access via: **Menu > Projects & Time Tracking**

### Views

| View | URL | Description |
|------|-----|-------------|
| Dashboard | `/m/projects/dashboard/` | Project overview and time tracking summary |
| Projects | `/m/projects/projects/` | Create and manage projects |
| Time Entries | `/m/projects/time/` | Log and manage time entries |
| Settings | `/m/projects/settings/` | Module configuration |

## Models

| Model | Description |
|-------|-------------|
| `Project` | Project record with name, code, description, status, start/end dates, budget, and spent amount |
| `TimeEntry` | Time log entry linked to a project with employee reference, date, hours, description, and billable flag |

## Permissions

| Permission | Description |
|------------|-------------|
| `projects.view_project` | View projects |
| `projects.add_project` | Create new projects |
| `projects.change_project` | Edit project details |
| `projects.delete_project` | Delete projects |
| `projects.view_timeentry` | View time entries |
| `projects.add_timeentry` | Log new time entries |
| `projects.change_timeentry` | Edit time entries |
| `projects.manage_settings` | Access and modify module settings |

## License

MIT

## Author

ERPlora Team - support@erplora.com
