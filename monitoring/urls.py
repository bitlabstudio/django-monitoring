"""URLs for the monitoring app."""
from django.conf.urls.defaults import patterns, url

from . import monitor
from . import views


urlpatterns = patterns(
    '',
    url(r'^$',
        views.MonitoringView.as_view(),
        name='monitoring_view'),
)

for monitor_name, monitor_view in monitor.get_all():
    urlpatterns += patterns(
        '',
        url(r'^ajax/{0}/$'.format(monitor_name),
            monitor_view,
            name=monitor.get_view_name(monitor_name)),
    )
