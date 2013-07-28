"""URLs for the monitoring app."""
from django.conf.urls.defaults import patterns, url

from . import views


urlpatterns = patterns(
    '',
    url(r'^$',
        views.MonitoringView.as_view(),
        name='monitoring_view'),
)
