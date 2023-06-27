import json

from django.http import HttpResponse
from django.shortcuts import redirect, render
from rest_framework import generics, status
from rest_framework.response import Response
from tasks import forms
from tasks.models import Subject, Task
from tasks.serializers import TaskSerializer


# Create your views here.
def homepage(request):
    tasks = Task.objects.all().order_by("-created")[0:6]
    return render(
        request,
        "tasks/homepage.html",
        {
            "title": "TasksMaster homepage",
            "tasks": tasks,
        },
    )


# API GET


def get_tasks_API(request, id=None):
    if id is not None:
        return get_task_by_id(request, id)
    else:
        return get_all_tasks(request)


def get_all_tasks(request):
    tasks = Task.objects.all()
    task_list = []
    for task in tasks:
        task_data = {
            "title": task.title,
            "subject": task.subject.name,
            "due_date": str(task.due_date),
            "urgent": task.urgent,
            "priority": task.priority,
            "created": str(task.created),
            "updated": str(task.updated),
            # Agrega otros campos según sea necesario
        }
        task_list.append(task_data)

    return HttpResponse(json.dumps(task_list), content_type="application/json")


def get_task_by_id(request, id):
    try:
        task = Task.objects.get(pk=id)
        task_data = {
            "title": task.title,
            "subject": task.subject.name,
            "due_date": str(task.due_date),
            "urgent": task.urgent,
            "priority": task.priority,
            "created": str(task.created),
            "updated": str(task.updated),
            # Agrega otros campos según sea necesario
        }
        return HttpResponse(
            json.dumps(task_data), content_type="application/json", status=200
        )
    except Task.DoesNotExist:
        error_data = {
            "status": {
                "type": "error",
                "code": 404,
                "message": "The requested task could not be found",
            }
        }
        return HttpResponse(
            json.dumps(error_data), content_type="application/json", status=404
        )


# API POST


class TaskCreateAPIView(generics.CreateAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer

    def create(self, request, *args, **kwargs):
        # Formato invalido
        if request.content_type != "application/json":
            error_response = {
                "status": {
                    "type": "error",
                    "code": status.HTTP_400_BAD_REQUEST,
                    "message": "Malformed body: only valid JSON is accepted",
                }
            }
            return Response(error_response, status=status.HTTP_400_BAD_REQUEST)

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # Tarea Existente
        task_name = serializer.validated_data.get("title")
        due_date = serializer.validated_data.get("due_date")

        if Task.objects.filter(title=task_name, due_date=due_date).exists():
            error_response = {
                "status": {
                    "type": "error",
                    "code": status.HTTP_409_CONFLICT,
                    "message": "A task with the same name and due date already exists",
                }
            }
            return Response(error_response, status=status.HTTP_409_CONFLICT)

        # Crear Tarea
        self.perform_create(serializer)

        task_id = serializer.instance.id
        response_data = {
            "status": {
                "type": "ok",
                "code": status.HTTP_200_OK,
                "message": "Task created successfully",
            },
            "id": task_id,
        }
        return Response(response_data, status=status.HTTP_200_OK)


"""def create_task_API(request):
    if request.method == "POST":
        data = json.loads(request.body)
        title = data.get("title")
        subject = data.get("subject")
        due_date = data.get("due_date")
        urgent = data.get("urgent")
        priority = data.get("priority")

        # Realiza las validaciones y crea la tarea en la base de datos
        # ...

        # Retorna la respuesta adecuada, por ejemplo, un código de estado HTTP 201
        return HttpResponse(status=201)
    else:
        return HttpResponse(status=405)  # Método no permitido (solo se permite POST)
"""


def list_tasks(request):
    tasks = Task.objects.all()
    return render(
        request,
        "tasks/list_task.html",
        {
            "title": "Tareas Activas",
            "tasks": tasks,
        },
    )


def list_subjects(request):
    subjects = Subject.objects.all()
    return render(
        request,
        "tasks/list_subjects.html",
        {
            "title": "Temas",
            "subjects": subjects,
        },
    )


def subject_detail(request, pk):
    subject = Subject.objects.get(pk=pk)
    return render(
        request,
        "tasks/subject_detail.html",
        {
            "tittle": f"Tema{subject.name}",
            "subject": subject,
        },
    )


def list_by_priority(request, priority):
    priority = priority[0].upper()
    tasks = Task.objects.filter(priority=priority)
    return render(
        request,
        "tasks/list_task.html",
        {
            "title": f"Tareas de prioridad {priority}",
            "tasks": tasks,
        },
    )


"""
def list_high_priority(request):
    tasks = Task.objects.filter(priority="H")
    return render(
        request,
        "tasks/list_task.html",
        {
            "title": "Tareas de prioridad alta",
            "tasks": tasks,
        },
    )
def list_low_priority(request):
    tasks = Task.objects.filter(priority="L")
    return render(
        request,
        "tasks/list_task.html",
        {
            "title": "Tareas de prioridad Baja",
            "tasks": tasks,
        },
    )
def list_normal_priority(request):
    tasks = Task.objects.filter(priority="N")
    return render(
        request,
        "tasks/list_task.html",
        {
            "title": "Tareas de prioridad normal",
            "tasks": tasks,
        },
    )
"""


def search(request):
    tasks = []
    query = ""
    if request.method == "POST":
        form = forms.SearchForm(request.POST)
        if form.is_valid():
            query = form.cleaned_data["query"]
            tasks = Task.objects.filter(title__icontains=query)
            priority = form.cleaned_data.get("priority") or []
            if priority:
                tasks = tasks.filter(priority__in=priority)
                urgent = form.cleaned_data.get("urgent", False)
            if urgent:
                tasks = tasks.filter(urgent=True)
    else:
        form = forms.SearchForm()

    return render(
        request,
        "tasks/search.html",
        {
            "title": "Buscar tareas",
            "form": form,
            "tasks": tasks,
            "query": query,
        },
    )
    """ query = request.POST.get("query")
    if query:
        query = request.GET.get("query", "")

    tasks = Task.objects.filter(title__icontains=query)
    priorities = request.POST.getlist("priority")
    if priorities:
        tasks = tasks.filter(priority__in=priorities)
 """


def list_tasks_per_year(request, year):
    tasks = Task.objects.filter(created__year=year)
    return render(
        request,
        "tasks/list_task.html",
        {
            "title": f"Tareas creadas en el año {year}",
            "tasks": tasks,
        },
    )


def lab_view(request):
    return render(request, "tasks/lab.html", {"title": "Labs page"})


def edit_task(request, pk):
    task = Task.objects.get(pk=pk)
    if request.method == "POST":
        form = forms.EditTaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            return redirect("/")
    else:
        form = forms.EditTaskForm(instance=task)
    return render(
        request,
        "tasks/edit_task.html",
        {
            "title": f"Editar tarea #{task.pk}",
            "form": form,
        },
    )


def create_task(request):
    if request.method == "POST":
        form = forms.CreateTaskForm(request.POST)
        if form.is_valid():
            new_task = form.save()
            return redirect("/")
    else:
        form = forms.CreateTaskForm()
    return render(
        request,
        "tasks/create_task.html",
        {
            "title": "Nueva tarea",
            "form": form,
        },
    )


"""
      ModelA.objects.filter(num__gt=23)  # num > 23
    ModelA.objects.filter(num__gte=23) # num >= 23
    ModelA.objects.filter(num__lt=23)  # num < 23
    ModelA.objects.filter(num__lte=23) # num <= 23
    ModelA.objects.exclude(num=23) # num != 23

    hoy = datetime...
    ModelA.objects.filter(fecha=hoy)
    ModelA.objects.filter(fecha__gt=hoy)
    ModelA.objects.filter(fecha__year=2023)
    ModelA.objects.filter(fecha__year__gte=2023)
    ModelA.objects.filter(fecha__month=2)
    ModelA.objects.filter(fecha__month__gte=10)
    ModelA.objects.filter(fecha__year=2023).filter(fecha__month=2)

    txt = str()
    ModelA.objects.filter(texto=txt)
    ModelA.objects.filter(texto__gt=txt)
    ModelA.objects.filter(texto__contains=txt)
    ModelA.objects.filter(texto__icontains=txt)
    ModelA.objects.filter(texto__startwith=txt)
    ModelA.objects.filter(texto__istartwith=txt)

    tasks = Task.objects.filter(priority="l").filter(priority="n")

    tasks = Task.objects.exclude(priority="h")
    tasks = Task.objects.filter(priority__in=["l", "n"])

    tasks = Task.objects.filter(subject__name="core")
    """
