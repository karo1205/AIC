from django.contrib import admin
from polls.models import Task, Worker


class TaskAdmin(admin.ModelAdmin):

    """This class controls the admin interface for Tasks."""

    list_display = ('id', 'worker', 'callback_uri', 'question', 'answer', 'data')


admin.site.register(Worker)
admin.site.register(Task, TaskAdmin)
# Register your models here.
