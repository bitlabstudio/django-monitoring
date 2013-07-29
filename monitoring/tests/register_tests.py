"""Tests for the register facilities of the monitoring app."""
from django.test import TestCase

from ..exceptions import MonitoringRegistryException
from ..register import MonitoringRegistry
from ..views import IntegerCountView
from test_app.models import UserLoginCount


class DummyClass(object):
    """Just a class so that we have something to register."""
    pass


class MonitoringRegistryTestCase(TestCase):
    """Tests for the ``MonitoringRegistry`` class."""
    longMessage = True

    def setUp(self):
        super(MonitoringRegistryTestCase, self).setUp()
        self.monitor = MonitoringRegistry()
        self.monitor.__init__()

    def tearDown(self):
        self.monitor.__init__()

    def test_get_model_class(self):
        self.monitor.register(
            'foobar', IntegerCountView.as_view(model=UserLoginCount))
        view_func = self.monitor._registered_monitors.get('foobar')
        result = self.monitor._get_model_class(view_func)
        self.assertEqual(result, UserLoginCount, msg=(
            'Internal helper method, should return the model class of a given'
            ' view function.'))

    def test_get_model_class_with_no_model(self):
        """
        Should raise exception when the given view func has no model defined.

        """
        self.assertRaises(
            MonitoringRegistryException,
            self.monitor.register,
            'barfoo',
            IntegerCountView.as_view(),
        )

    def test_get_view_name(self):
        self.monitor.register(
            'foobar', IntegerCountView.as_view(model=UserLoginCount))
        expected = 'monitoring_{0}'.format(UserLoginCount.__name__.lower())
        result = self.monitor.get_view_name('foobar')
        self.assertEqual(result, expected, msg=(
            'Should return the view name based on the model name'))

    def test_get_view_name_with_view_name_set(self):
        self.monitor.register(
            'foobar', IntegerCountView.as_view(
                model=UserLoginCount, view_name='foobar_view'))
        expected = 'foobar_view'
        result = self.monitor.get_view_name('foobar')
        self.assertEqual(result, expected, msg=(
            'Should return the view name as specified on the view'))

    def test_get(self):
        self.monitor.register(
            'foobar', IntegerCountView.as_view(model=UserLoginCount))
        result = self.monitor.get('foobar')
        self.assertEqual(result, UserLoginCount, msg=(
            'Should return the monitor class for the given monitor'))

    def test_register(self):
        self.monitor.register(
            'foobar', IntegerCountView.as_view(model=UserLoginCount))
        self.assertEqual(len(self.monitor._registered_monitors), 1, msg=(
            'Should add the new monitor to the singleton'))

    def test_register_twice(self):
        """Should raise exception when this monitor is already registered."""
        self.monitor.register(
            'foobar', IntegerCountView.as_view(model=UserLoginCount))
        self.assertRaises(
            MonitoringRegistryException,
            self.monitor.register,
            'foobar',
            IntegerCountView.as_view(model=UserLoginCount),
        )

    def test_register_wrong_base_class(self):
        """
        Should raise exception when this monitor's class has wron base class.

        All monitors should be derived from ``MonitoringBase``.

        """
        self.assertRaises(
            MonitoringRegistryException,
            self.monitor.register,
            'foobar',
            IntegerCountView.as_view(model=DummyClass),
        )

    def test_unregister(self):
        self.monitor.register(
            'foobar', IntegerCountView.as_view(model=UserLoginCount))
        self.monitor.unregister('foobar')
        self.assertEqual(len(self.monitor._registered_monitors), 0, msg=(
            'Should remove the monitor from the singleton'))

        self.assertRaises(
            MonitoringRegistryException,
            self.monitor.unregister,
            'foobar',
        )
