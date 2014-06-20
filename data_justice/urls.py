from django.conf.urls import patterns, include, url
from django.views.generic import TemplateView
from django.contrib import admin



admin.autodiscover()

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^', include('home.urls', namespace='home')),
    url(r'^download/', include('download.urls', namespace='download')),
    url(r'^feedback/', include('feedback.urls', namespace='feedback')),
    url(r'^api/', include('api.urls', namespace='api')),
    url(r'^apps/', include('apps.urls', namespace='apps')),
)
