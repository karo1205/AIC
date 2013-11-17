from django.contrib import admin
from polls.models import Task, Worker

admin.site.register(Worker)
admin.site.register(Task)
# Register your models here.
