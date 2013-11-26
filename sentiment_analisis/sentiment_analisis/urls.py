from django.conf.urls import patterns, include, url
from tastypie.api import Api
from analysis.api.resources import TaskResource

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

v1_api = Api(api_name='v1')
v1_api.register(TaskResource())

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'sentiment_analisis.views.home', name='home'),
    # url(r'^sentiment_analisis/', include('sentiment_analisis.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^query/', include('analysis.urls', namespace="analysis")),
    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    (r'^api/', include(v1_api.urls))
)
