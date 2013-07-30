"""Views for the monitoring app."""
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic import ListView, TemplateView

from . import monitor


class MonitoringViewMixin(object):
    """Helper methods that all monitoring base views need."""
    view_name = None

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):  # pragma: no cover
        return super(MonitoringViewMixin, self).dispatch(
            request, *args, **kwargs)

    def get_template_names(self):
       """
       Returns the template name for the view based on the view's model.

       """
       return ['monitoring/{0}.html'.format(self.model.__name__.lower()), ]

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
    pass


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
