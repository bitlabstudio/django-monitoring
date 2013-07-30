"""URLs for the monitoring app."""
from django.conf.urls.defaults import patterns, url

from .register import monitor
from . import views


def autodiscover(urlpatterns):
    """Adds AJAX urls for the views of all registered monitors."""
    for monitor_name, monitor_view in monitor.get_all():
        urlpatterns += patterns(
            '',
            url(r'^ajax/{0}/$'.format(monitor_name),
                monitor_view,
                name=monitor.get_view_name(monitor_name)),
        )
    return urlpatterns


default_patterns = patterns(
    '',
    url(r'^$',
        views.MonitoringView.as_view(),
        name='monitoring_view'),
)


urlpatterns = default_patterns
urlpatterns = autodiscover(urlpatterns)
