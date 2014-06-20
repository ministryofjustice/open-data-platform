from django.conf.urls import patterns, url
from django.views.generic import TemplateView

urlpatterns = patterns('',
    url(r'^$', TemplateView.as_view(template_name='home/index.html'), name='index'),
    url(r'^doc/$', TemplateView.as_view(template_name='home/doc.html'), name='doc'),
)
