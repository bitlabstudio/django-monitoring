"""Tests for the register facilities of the monitoring app."""
from django.test import TestCase

from ..exceptions import MonitoringRegistryException
from ..register import MonitoringRegistry
from test_app.models import UserCount


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

    def test_register(self):
        self.monitor.register('foobar', UserCount)
        self.assertEqual(len(self.monitor._registered_monitors), 1, msg=(
            'Should add the new monitor to the singleton'))

    def test_register_twice(self):
        """Should raise exception when this monitor is already registered."""
        self.monitor.register('foobar', UserCount)
        self.assertRaises(
            MonitoringRegistryException,
            self.monitor.register,
            'foobar',
            UserCount,
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
            DummyClass,
        )

    def test_unregister(self):
        self.monitor.register('foobar', UserCount)
        self.monitor.unregister('foobar')
        self.assertEqual(len(self.monitor._registered_monitors), 0, msg=(
            'Should remove the monitor from the singleton'))

        self.assertRaises(
            MonitoringRegistryException,
            self.monitor.unregister,
            'foobar',
        )
