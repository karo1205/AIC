from django.contrib.auth.models import User
from tastypie import fields
from tastypie.resources import ModelResource
from polls.models import Task, Worker
from tastypie.authorization import Authorization
import logging
logger = logging.getLogger(__name__)

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
        allowed_methods = ['get', 'post', 'delete']
        resource_name = 'task'
        #authorization = DjangoAuthorization()
        authorization = Authorization()

    def dehydrate(self, bundle):
        bundle.data['callback_uri'] += "?format=json"
        return bundle


class TestResource(ModelResource):

    """Docstring."""

    name = fields.CharField(attribute='name')
    age = fields.IntegerField(attribute='years_old', null=True)

    class Meta:
        #queryset = Task.objects.all()
        #queryset = None
        allowed_methods = ['get', 'post']
        resource_name = 'test'
        #authorization = DjangoAuthorization()
        #authorization = Authorization()

    def hydrate(self, bundle):
        logger.info(bundle.data['name'])
        logger.info(str(bundle.data['age']))
        return bundle
