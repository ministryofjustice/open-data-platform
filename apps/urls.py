from django.conf.urls import patterns, url
from django.views.generic import TemplateView
from apps import views

urlpatterns = patterns('',
    url(r'^$', TemplateView.as_view(template_name='apps/index.html'), name='index'),
    url(r'^outcome$', views.OutcomeView.as_view(), name='outcome'),
)
