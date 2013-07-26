"""
Singleton class that can collect registered monitors on server start.

When writing tests that involve the monitor, make sure to call ``__init__``
in your ``setUp`` and ``teardown`` methods, otherwise montors that have been
added in your tests will still be available in later tests.

"""
from .exceptions import MonitoringRegistryException


class Singleton(type):
    """Makes sure that we store registered models at one central place."""
    def __init__(mcs, name, bases, dict_):
        super(Singleton, mcs).__init__(name, bases, dict_)
        mcs.instance = None

    def __call__(mcs, *args, **kwargs):
        if mcs.instance is None:
            mcs.instance = super(
                Singleton, mcs).__call__(*args, **kwargs)
        return mcs.instance


class MonitoringRegistry(object):
    __metaclass__ = Singleton

    def __init__(self, *args, **kwargs):
        self._registered_monitors = {}

    def register(self, monitor_name, model_class):
        """
        Registers a monitor on server start.

        :param monitor_name: A unique monitor name.
        :param model_class: A Django model that will hold the data points for
          the monitor.

        """
        if monitor_name in self._registered_monitors.keys():
            raise MonitoringRegistryException(
                'A monitor with this name has already been registered')
        self._registered_monitors[monitor_name] = model_class

    def unregister(self, monitor_name):
        """
        Unregisters a monitor.

        :param monitor_name: Name of the monitor which should be unregistered.

        """
        try:
            monitor = self._registered_monitors.pop(monitor_name)
        except KeyError:
            raise MonitoringRegistryException(
                '{0} is not registered with moderation.'.format(monitor_name))
