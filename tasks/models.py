from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone

PRIORITIES = [
    ("L", "Prioridad baja"),
    ("N", "Prioridad normal"),
    ("H", "Prioridad alta"),
]


def fecha_en_futuro(value):
    if value:
        if value < timezone.now().date():
            raise ValidationError("La fecha de entrega debe ser fecha futura ")


class Subject(models.Model):
    class Meta:
        verbose_name = "Asignatura"
        verbose_name_plural = "Asignaturas"

    id = models.AutoField(primary_key=True)
    name = models.CharField(
        verbose_name="Nombre de la asignatura", max_length=120, unique=True
    )

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Task(models.Model):
    class Meta:
        verbose_name = "Tarea"
        verbose_name_plural = "Tareas"

    # id = models.AutoField(primary_key=True) se crea automaticamente,no hace falta
    title = models.CharField(
        "Título",
        max_length=250,
        unique=True,
    )
    subject = models.ForeignKey(
        Subject,
        verbose_name="Asignatura",
        on_delete=models.PROTECT,
        related_name="tasks",
        default=1,
    )
    due_date = models.DateField(
        "Dia de entrega",
        null=True,
        blank=True,
        default=None,
        validators=[fecha_en_futuro],
    )
    urgent = models.BooleanField(default=False)
    priority = models.CharField(
        "Prioridad", max_length=1, choices=PRIORITIES, default="N"
    )
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Tarea #{self.pk}: {self.title}"
