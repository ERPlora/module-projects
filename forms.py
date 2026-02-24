from django import forms
from django.utils.translation import gettext_lazy as _

from .models import Project

class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['name', 'code', 'description', 'status', 'start_date', 'end_date', 'budget', 'spent']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'input input-sm w-full'}),
            'code': forms.TextInput(attrs={'class': 'input input-sm w-full'}),
            'description': forms.Textarea(attrs={'class': 'textarea textarea-sm w-full', 'rows': 3}),
            'status': forms.Select(attrs={'class': 'select select-sm w-full'}),
            'start_date': forms.TextInput(attrs={'class': 'input input-sm w-full', 'type': 'date'}),
            'end_date': forms.TextInput(attrs={'class': 'input input-sm w-full', 'type': 'date'}),
            'budget': forms.TextInput(attrs={'class': 'input input-sm w-full', 'type': 'number'}),
            'spent': forms.TextInput(attrs={'class': 'input input-sm w-full', 'type': 'number'}),
        }

