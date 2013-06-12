from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.conf import settings


urlpatterns = patterns('authdetails.views',
    url(r'^$', 'login_view', name='home'),
    url(r'^usercreation/', 'user_creation', name='home'),
    url(r'^logout', 'logout_view', name='logout'),
)