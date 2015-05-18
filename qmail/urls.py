from django.conf.urls import patterns, include, url
urlpatterns = patterns('',
    url(r'^$', 'qmail.views.home', name='home'),
)
