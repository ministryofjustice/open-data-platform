from django.conf.urls import patterns, url
from django.views.generic import TemplateView

urlpatterns = patterns('',
    url(r'^$', TemplateView.as_view(template_name='feedback/index.html'), name='index'),
    url(r'^thanks/$', TemplateView.as_view(template_name='feedback/thanks.html'), name='thanks'),
)
