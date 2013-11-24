from django.contrib.auth.models import User
from tastypie import fields
from tastypie.resources import ModelResource
from polls.models import Task, Worker
from tastypie.authorization import Authorization


class UserResource(ModelResource):

    """Docstring."""

    class Meta:
        queryset = User.objects.all()
        resource_name = 'user'


class WorkerResource(ModelResource):

    """Docstring."""

    class Meta:
        queryset = Worker.objects.all()
        allowed_methods = ['get']
        resource_name = 'worker'
        #authorization = DjangoAuthorization()
        authorization = Authorization()


class TaskResource(ModelResource):

    """Docstring."""

    worker = fields.ForeignKey(WorkerResource, 'worker')

    class Meta:
        queryset = Task.objects.all()
        allowed_methods = ['get', 'post']
        resource_name = 'task'
        #authorization = DjangoAuthorization()
        authorization = Authorization()


