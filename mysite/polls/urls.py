from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.conf import settings

from django.conf.urls import patterns, include, url

urlpatterns = patterns('polls.views',
    url(r'^$', 'login', name='home'),
    url(r'^usercreation/', 'user_creation', name='home'),
    url(r'^index/$', 'index', name="index"),
    url(r'^polls/(?P<poll_id>\d+)/$', 'detail', name="detail"),
    url(r'^polls/(?P<poll_id>\d+)/results/$', 'results', name="results"),
    url(r'^polls/(?P<poll_id>\d+)/vote/$', 'vote', name="vote"),
)