from django.contrib.auth.models import User
#from tastypie import fields
from tastypie.resources import ModelResource
from polls.models import Task
from tastypie.authorization import Authorization

class TaskResource(ModelResource):

    """Docstring."""

    class Meta:
        queryset = Task.objects.all()
        allowed_methods = ['get','post']
        resource_name = 'task'
        #authorization = DjangoAuthorization()
        authorization = Authorization()

class UserResource(ModelResource):

    """Docstring."""

    class Meta:
        queryset = User.objects.all()
        resource_name = 'user'
