from django.conf.urls import patterns, url
from download import views
from django.views.generic import TemplateView

urlpatterns = patterns('',
    url(r'^$',     TemplateView.as_view(template_name='download/index.html'), name='index'),
    url(r'^go/$',  views.GoView.as_view(), name='go'),
)
