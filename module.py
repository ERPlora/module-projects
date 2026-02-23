    from django.utils.translation import gettext_lazy as _

    MODULE_ID = 'projects'
    MODULE_NAME = _('Projects & Time Tracking')
    MODULE_VERSION = '1.0.0'
    MODULE_ICON = 'git-branch-outline'
    MODULE_DESCRIPTION = _('Project management, milestones and time tracking')
    MODULE_AUTHOR = 'ERPlora'
    MODULE_CATEGORY = 'operations'

    MENU = {
        'label': _('Projects & Time Tracking'),
        'icon': 'git-branch-outline',
        'order': 55,
    }

    NAVIGATION = [
        {'label': _('Dashboard'), 'icon': 'speedometer-outline', 'id': 'dashboard'},
{'label': _('Projects'), 'icon': 'git-branch-outline', 'id': 'projects'},
{'label': _('Time Entries'), 'icon': 'time-outline', 'id': 'time'},
{'label': _('Settings'), 'icon': 'settings-outline', 'id': 'settings'},
    ]

    DEPENDENCIES = []

    PERMISSIONS = [
        'projects.view_project',
'projects.add_project',
'projects.change_project',
'projects.delete_project',
'projects.view_timeentry',
'projects.add_timeentry',
'projects.change_timeentry',
'projects.manage_settings',
    ]
