from django.shortcuts import render
from tasks import forms
from tasks.models import Subject, Task


# Create your views here.
def homepage(request):
    return render(
        request,
        "tasks/homepage.html",
        {
            "title": "TasksMaster homepage",
        },
    )


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


def create_task(request):
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
