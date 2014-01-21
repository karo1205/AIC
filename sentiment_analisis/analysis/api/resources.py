from tastypie import fields
from tastypie.resources import ModelResource
from analysis.models import Task
from tastypie.authorization import Authorization
import logging
logger = logging.getLogger(__name__)


class TaskResource(ModelResource):

    """Docstring."""

    data = fields.CharField(attribute='data', default='default')

    class Meta:
        queryset = Task.objects.filter(status='S')
        allowed_methods = ['get', 'put']
        resource_name = 'task'
        excludes = ['com_date',
                    'id',
                    'orphaned',
                    'pub_date',
                    # 'status',
                    'price',
                    'callback_uri']
        #authorization = DjangoAuthorization()
        authorization = Authorization()

    def dehydrate_data(self, bundle):
        return "{data:data}"

    def hydrate(self,bundle):
        bundle.data['status'] = 'DONE'
        logger.error("callback" + bundle.data['status'])
        return bundle
