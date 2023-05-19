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
        widget=forms.CheckboxSelectMultiple,
        choices=PRIORITIES,
    )
    urgent = forms.BooleanField(
        label="Urgente",
        required=False,
    )


def fecha_en_futuro(value):
    from django.core.exceptions import ValidationError
    from django.utils import timezone

    if value:
        if value < timezone.now().date():
            raise ValidationError("La fecha de entrega debe ser fecha futura ")


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

    due_date = forms.DateField(
        validators=[
            fecha_en_futuro,
        ]
    )


class EditTaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = [
            "title",
            "subject",
            "due_date",
            "priority",
            "urgent",
        ]

    def clean(self):
        cleaned_data = super().clean()
        due_date = cleaned_data["due_date"]
        fecha_en_futuro(due_date)
        return cleaned_data
