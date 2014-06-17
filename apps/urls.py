from django.conf.urls import patterns, url
from django.views.generic import TemplateView

urlpatterns = patterns('',
    url(r'^$', TemplateView.as_view(template_name='apps/index.html'), name='index'),
    url(r'^demo1$', TemplateView.as_view(template_name='apps/demo1.html'), name='demo1')
)
