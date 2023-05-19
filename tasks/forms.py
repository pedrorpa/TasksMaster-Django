from django import forms
from tasks.models import Task

PRIORITIES = [
    ("L", "Prioridad baja"),
    ("N", "Prioridad normal"),
    ("H", "Prioridad alta"),
]


class SearchForm(forms.Form):
    query = forms.CharField(
        label="Buscar",
        required=False,
    )
    priority = forms.MultipleChoiceField(
        label="Prioridad",
        required=False,
        choices=PRIORITIES,
    )
    urgent = forms.BooleanField(
        label="Urgente",
        required=False,
    )


class CreateTaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = [
            "title",
            "subject",
            "due_date",
            "priority",
            "urgent",
        ]
