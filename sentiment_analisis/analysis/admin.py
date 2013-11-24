"""This Modules controls the admin interface of tha analysis app."""


from django.contrib import admin
from analysis.models import Feed, Keyword, Worker, Task, Sentiment
# Register your models here.


class TaskAdmin(admin.ModelAdmin):

    """This class controls the admin interface for Tasks."""

    list_display = ('id', 'task_uri', 'question', 'answer', 'status')


class FeedAdmin(admin.ModelAdmin):

    """This class controls the admin interface for Feeds."""

    list_display = ('title', 'link')


class WorkerAdmin(admin.ModelAdmin):

    """This class controls the admin interface for Feeds."""

    list_display = ('id', 'worker_uri')


admin.site.register(Feed, FeedAdmin)
admin.site.register(Keyword)
admin.site.register(Worker, WorkerAdmin)
admin.site.register(Task, TaskAdmin)
admin.site.register(Sentiment)
