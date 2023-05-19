from django.contrib import admin
from tasks.models import Subject, Task


class AdminSubject(admin.ModelAdmin):
    list_display = ["pk", "name"]


admin.site.register(Subject, AdminSubject)


class AdminTask(admin.ModelAdmin):
    date_hierarchy = "due_date"
    list_display = ["pk", "title", "subject", "priority"]


admin.site.register(Task, AdminTask)
# Register your models here.
