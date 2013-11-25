from django.conf.urls import patterns, include, url
from django.contrib import admin
from tastypie.api import Api
from polls.api.resources import TaskResource, UserResource, WorkerResource, TestResource

admin.autodiscover()

v1_api = Api(api_name='v1')
v1_api.register(TaskResource())
v1_api.register(UserResource())
v1_api.register(WorkerResource())
v1_api.register(TestResource())

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    # Examples, TestResource:
    # url(r'^$', 'crowdsource_sim.views.home', name='home'),
    # url(r'^crowdsource_sim/', include('crowdsource_sim.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^polls/', include('polls.urls', namespace="polls")),
    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    (r'^api/', include(v1_api.urls))
)
