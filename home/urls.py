from django.conf.urls import patterns, url
from django.views.generic import TemplateView
from home import views

urlpatterns = patterns('',
    url(r'^$', TemplateView.as_view(template_name='home/index.html'), name='index'),
    url(r'^doc/$', TemplateView.as_view(template_name='home/doc.html'), name='doc'),
    url(r'^outcome/(?P<outcome_id>[0-9]+)?$', views.OutcomeView.as_view(), name='outcome'),
)
