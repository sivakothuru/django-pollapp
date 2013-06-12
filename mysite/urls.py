from django.conf.urls import patterns, include, url
from django.views.generic import TemplateView
# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    
    # url(r'^mysite/', include('mysite.foo.urls')),
    #url(r'^accounts/profile/', TemplateView.as_view(template_name='profile.html'), name="home"),

    #(r'^accounts/', include('allauth.urls')),
    url(r'^', include('authdetails.urls')),
    url(r'^', include('polls.urls')),
    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)
