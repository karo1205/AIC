from django.conf.urls import patterns, url

from analysis import views

urlpatterns = patterns('',
    url(r'^$', views.query, name='query'),
#    url(r'^result/$', views.result, name='result')
    url(r'^confirm/$', views.confirm, name='confirm'),
    url(r'^error/$', views.error, name='error'),
    url(r'^(?P<order_id>\d+)/$', views.result, name='result')
    
)
