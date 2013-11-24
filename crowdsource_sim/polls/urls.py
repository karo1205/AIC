from django.conf.urls import patterns, url

from polls import views

urlpatterns = patterns('',
    # ex: /polls/
    url(r'^$', views.index, name='index'),
    # ex: /polls/5/
    url(r'^(?P<task_id>\d+)/$', views.detail, name='detail'),
    # ex: /polls/5/results/
    url(r'^(?P<task_id>\d+)/results/$', views.results, name='results'),
    # ex: /polls/5/submit/
    url(r'^(?P<task_id>\d+)/submit/$', views.submit, name='submit'),
)
