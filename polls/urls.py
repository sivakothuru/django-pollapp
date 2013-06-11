from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.conf import settings

from django.conf.urls import patterns, include, url

urlpatterns = patterns('polls.views',
    url(r'^$', 'login_view', name='home'),
    url(r'^usercreation/', 'user_creation', name='home'),
    url(r'^index/$', 'index', name="index"),
    url(r'^polls/(?P<poll_id>\d+)/$', 'detail', name="detail"),
    url(r'^polls/(?P<poll_id>\d+)/results/$', 'results', name="results"),
    url(r'^polls/(?P<poll_id>\d+)/vote/$', 'vote', name="vote"),
    url(r'^logout', 'logout_view', name='logout'),
    url(r'^(?P<poll_id>\d+)/votes_of_mine', 'votes_of_a_user', name='myvotes')
)