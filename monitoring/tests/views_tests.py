"""Tests for the views of the monitoring app."""
from django.contrib.auth.models import AnonymousUser
from django.test import RequestFactory, TestCase

from django_libs.tests.mixins import ViewTestMixin
from django_libs.tests.factories import UserFactory

from .. import monitor
from ..views import MonitoringView
from .test_app.models import UserLoginCount


class MonitoringViewTestCase(ViewTestMixin, TestCase):
    """Tests for the ``MonitoringView`` view."""
    longMessage = True

    def setUp(self):
        super(MonitoringViewTestCase, self).setUp()
        monitor.__init__()
        monitor.register('user_login_count', UserLoginCount)
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

    def test_load_view(self):
        self.should_be_callable_when_authenticated(self.user)

    def test_login_required(self):
        req, view = self.get_req_and_view()
        req.user = AnonymousUser()
        resp = view.dispatch(req)
        self.assertEqual(resp.status_code, 302, msg=(
            'Should redirect to login if not authenticated'))
