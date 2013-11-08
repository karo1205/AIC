"""Tastypie Resources."""
from tastypie.resources import ModelResource
from polls.models import Poll


class PollResource(ModelResource):

    """This is tastypie resource for polls"""

    class Meta:
        queryset = Poll.objects.all()
        resource_name = 'polls'
        allowed_methods = ['get']
