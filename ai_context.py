"""
AI context for the Projects module.
Loaded into the assistant system prompt when this module's tools are active.
"""

CONTEXT = """
## Module Knowledge: Projects

### Models

**Project**
- `name` (str, required), `code` (str, optional short identifier), `description` (text)
- `status` choices: active | on_hold | completed | cancelled (default: active)
- `start_date`, `end_date` (dates, optional)
- `budget` (decimal, default 0), `spent` (decimal, default 0 — updated as costs are recorded)

**TimeEntry**
- `project` (FK → Project, CASCADE, related_name='time_entries')
- `employee_id` (UUID, indexed — references LocalUser), `employee_name` (str — denormalized for display)
- `date` (date), `hours` (decimal), `description` (str, optional), `is_billable` (bool, default True)

### Key Flows

1. **Create project**: set name, code, start_date/end_date, and budget. Status defaults to 'active'.
2. **Log time**: create TimeEntry linked to project with employee_id, employee_name, date, and hours. Mark is_billable accordingly.
3. **Track spend**: update Project.spent manually when costs are incurred (time entries do not auto-update spent).
4. **Hold/complete**: update status to 'on_hold' for paused projects, 'completed' when finished.

### Relationships

- TimeEntry → Project (CASCADE).
- `employee_id` is a raw UUID (no FK) — maps to LocalUser. `employee_name` is stored for display without join.
- No FK to customers or invoices in this module; link via external reference or notes.
"""
