from tastypie import fields
from tastypie.resources import ModelResource
from tastypie import fields
from analysis.models import Task
from tastypie.authorization import Authorization
import logging
logger = logging.getLogger(__name__)


class TaskResource(ModelResource):

    """Docstring."""
    data = fields.CharField(attribute='data',default='default')

    class Meta:
        queryset = Task.objects.all()
        allowed_methods = ['get', 'post']
        resource_name = 'task'
        excludes = ['com_date','id','orphaned','pub_date','status']
        #authorization = DjangoAuthorization()
        authorization = Authorization()

    def dehydrate_data(self, bundle):
        return "{data:data}"
