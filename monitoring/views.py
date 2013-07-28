"""Views for the monitoring app."""
from django.views.generic import TemplateView


class MonitoringView(TemplateView):
    template_name = 'monitoring/index.html'
