from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = patterns('',
    # Examples:
    url(r'^$', 'crossit.views.home', name='home'),
    url(r'^diary/', include('diary.urls')),
    url(r'^qmail/', include('qmail.urls')),
    url(r'^chkusr/', 'crossit.views.checkExist', name='checkExist'),
    url(r'^reg/', 'crossit.views.regUsr', name='regUsr'),
    url(r'^login/', 'crossit.views.loginUsr', name='loginUsr'),
    url(r'^logout/', 'crossit.views.UsrLogout', name='UsrLogout'),
    url(r'^main/', 'crossit.views.MainPage', name='MainPage'),
    url(r'^ueditor/',include('DjangoUeditor.urls' )),
    #url(r'^oa2/', include('oauth2_provider.urls', namespace='oauth2_provider')),
    url(r'^admin/', include(admin.site.urls)),
)+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
