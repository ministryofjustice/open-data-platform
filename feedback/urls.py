from django.conf.urls import patterns, url
from feedback import views
from django.views.generic import TemplateView

urlpatterns = patterns('',
    url(r'^$', TemplateView.as_view(template_name='feedback/index.html'), name='index'),
    url(r'^thanks/$', views.ThanksView.as_view(), name='thanks'),
)
