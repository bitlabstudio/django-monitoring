"""Views for the monitoring app."""
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView


class MonitoringView(TemplateView):
    template_name = 'monitoring/index.html'

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        self.request = request
        return super(MonitoringView, self).dispatch(
            request, *args, **kwargs)
