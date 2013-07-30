"""Tests for the views of the monitoring app."""
from django.contrib.auth.models import AnonymousUser
from django.test import RequestFactory, TestCase

from django_libs.tests.mixins import ViewTestMixin
from django_libs.tests.factories import UserFactory

from .. import monitor
from ..urls import urlpatterns  # NOQA
from ..views import IntegerCountView, MonitoringView, MonitoringViewMixin
from .test_app.models import UserLoginCount


class MonitoringViewMixinTestCase(TestCase):
    """Tests for the ``MonitoringViewMixin``."""
    longMessage = True

    def test_requires_login(self):
        req = RequestFactory().get('/')
        req.user = AnonymousUser()
        resp = MonitoringViewMixin().dispatch(req)
        self.assertEqual(resp.status_code, 302, msg=(
            'Should redirect to login if anonymous'))

    def test_get_template_names(self):
        view = MonitoringViewMixin()
        view.model = UserLoginCount
        expected = ['monitoring/{0}.html'.format(
            UserLoginCount.__name__.lower()), ]
        result = view.get_template_names()
        self.assertEqual(result, expected, msg=(
            'The template name should be the model name, lowered'))

    def test_get_view_name(self):
        view = MonitoringViewMixin()
        view.model = UserLoginCount
        expected = 'monitoring_{0}'.format(UserLoginCount.__name__.lower())
        result = view.get_view_name()
        self.assertEqual(result, expected, msg=(
            'The view name should be based on the model name, lowered'))

        view.view_name = 'foobar'
        result = view.get_view_name()
        self.assertEqual(result, view.view_name, msg=(
            'If view name has been set explicitly, that name should be'
            ' returned'))


class MonitoringViewTestCase(ViewTestMixin, TestCase):
    """Tests for the ``MonitoringView`` view."""
    longMessage = True

    def setUp(self):
        super(MonitoringViewTestCase, self).setUp()
        monitor.__init__()
        monitor.register(
            'user_login_count', IntegerCountView.as_view(model=UserLoginCount))
        self.user = UserFactory()
        self.login(self.user)

    def tearDown(self):
        super(MonitoringViewTestCase, self).tearDown()
        monitor.__init__()

    def get_view_name(self):
        return 'monitoring_view'

    def get_req_and_view(self):
        """
        Helper method to create the fake request and instantiate the view.

        """
        req = RequestFactory().get('/')
        req.user = self.user
        view = MonitoringView()
        return req, view

    def test_login_required(self):
        req, view = self.get_req_and_view()
        req.user = AnonymousUser()
        resp = view.dispatch(req)
        self.assertEqual(resp.status_code, 302, msg=(
            'Should redirect to login if not authenticated'))

    def test_is_callable(self):
        self.should_be_callable_when_authenticated(self.user)
