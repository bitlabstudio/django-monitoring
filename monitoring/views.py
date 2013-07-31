"""Views for the monitoring app."""
from django.contrib.auth.decorators import login_required
from django.db.models import Count
from django.utils.decorators import method_decorator
from django.views.generic import ListView, TemplateView

from .register import monitor


class MonitoringViewMixin(object):
    """Helper methods that all monitoring base views need."""
    view_name = None
    monitor_title = None

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):  # pragma: no cover
        self.request = request
        return super(MonitoringViewMixin, self).dispatch(
            request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        ctx = super(MonitoringViewMixin, self).get_context_data(**kwargs)
        ctx.update({
            'monitor_title': self.monitor_title,
        })
        return ctx

    def get_template_names(self):
        """
        Returns the template name for the view based on the view's model.

        """
        return [self.model.get_template_name(), ]

    def get_view_name(self):
        """
        Returns the view name based on the view's model.

        If you have set the ``view_name`` attribute on the view, that will be
        returned instead.

        """
        if self.view_name is not None:
            return self.view_name
        return 'monitoring_{0}'.format(self.model.__name__.lower())


class IntegerCountView(MonitoringViewMixin, ListView):
    """Default view for the ``IntegerCountBase`` monitor model."""
    monitor_title = 'Integer Count'

    def get_queryset(self):
        qs = super(IntegerCountView, self).get_queryset()
        qs = qs.values('date_created').annotate(
            count=Count('date_created')).distinct()
        return qs


class MonitoringView(TemplateView):
    template_name = 'monitoring/index.html'

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        self.request = request
        return super(MonitoringView, self).dispatch(
            request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        ctx = super(MonitoringView, self).get_context_data(**kwargs)
        ctx.update({
            'monitor': monitor,
        })
        return ctx
