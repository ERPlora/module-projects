from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.core.models.base import HubBaseModel

PROJECT_STATUS = [
    ('active', _('Active')),
    ('on_hold', _('On Hold')),
    ('completed', _('Completed')),
    ('cancelled', _('Cancelled')),
]

class Project(HubBaseModel):
    name = models.CharField(max_length=255, verbose_name=_('Name'))
    code = models.CharField(max_length=20, blank=True, verbose_name=_('Code'))
    description = models.TextField(blank=True, verbose_name=_('Description'))
    status = models.CharField(max_length=20, default='active', choices=PROJECT_STATUS, verbose_name=_('Status'))
    start_date = models.DateField(null=True, blank=True, verbose_name=_('Start Date'))
    end_date = models.DateField(null=True, blank=True, verbose_name=_('End Date'))
    budget = models.DecimalField(max_digits=12, decimal_places=2, default='0', verbose_name=_('Budget'))
    spent = models.DecimalField(max_digits=12, decimal_places=2, default='0', verbose_name=_('Spent'))

    class Meta(HubBaseModel.Meta):
        db_table = 'projects_project'

    def __str__(self):
        return self.name


class TimeEntry(HubBaseModel):
    project = models.ForeignKey('Project', on_delete=models.CASCADE, related_name='time_entries')
    employee_id = models.UUIDField(db_index=True, verbose_name=_('Employee Id'))
    employee_name = models.CharField(max_length=255, verbose_name=_('Employee Name'))
    date = models.DateField(verbose_name=_('Date'))
    hours = models.DecimalField(max_digits=5, decimal_places=2, verbose_name=_('Hours'))
    description = models.CharField(max_length=255, blank=True, verbose_name=_('Description'))
    is_billable = models.BooleanField(default=True, verbose_name=_('Is Billable'))

    class Meta(HubBaseModel.Meta):
        db_table = 'projects_timeentry'

    def __str__(self):
        return str(self.id)

