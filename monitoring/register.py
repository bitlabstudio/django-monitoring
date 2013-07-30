"""
Singleton class that can collect registered monitors on server start.

When writing tests that involve the monitor, make sure to call ``__init__``
in your ``setUp`` and ``teardown`` methods, otherwise montors that have been
added in your tests will still be available in later tests.

"""
from .exceptions import MonitoringRegistryException
from .models import MonitoringBase


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

    def _get_model_class(self, view_func):
        """Helper method to retrieve the model from the view."""
        model_cls = view_func.func_closure[0].cell_contents.get('model')
        if model_cls is not None:
            return model_cls
        raise MonitoringRegistryException(
            'Cannot retrieve model from view {0}'.format(view_func.func_name))

    def get(self, monitor_name):
        """
        Returns the monitoring class for the given monitor name.

        :param monitor_name: :String representing the monitor name that has
          been used to register the monitor.

        """
        view_func = self._registered_monitors.get(monitor_name)
        return self._get_model_class(view_func)

    def get_all(self):
        """Returns all registered monitors."""
        return self._registered_monitors.items()

    def get_view_name(self, monitor_name):
        """
        Returns the view name for the given monitor.

        :param monitor_name: String representing the monitor name.

        """
        view_func = self._registered_monitors.get(monitor_name)
        view_name = view_func.func_closure[0].cell_contents.get('view_name')
        if view_name is not None:
            return view_name
        model = self._get_model_class(view_func)
        return 'monitoring_{0}'.format(model.__name__.lower())

    def register(self, monitor_name, monitor_view):
        """
        Registers a monitor on server start.

        :param monitor_name: A unique monitor name.
        :param monitor_view: A ListView that will display the data as a
          widget. Make sure to pass in something like
          ``IntegerCountView.as_view(model=YourModel)`` here.

        """
        if monitor_name in self._registered_monitors.keys():
            raise MonitoringRegistryException(
                'A monitor with this name has already been registered')

        model_cls = self._get_model_class(monitor_view)
        if not MonitoringBase in model_cls.mro():
            raise MonitoringRegistryException(
                'Monitor model class {0} must inherit MonitoringBase'.format(
                    model_cls.__name__))

        self._registered_monitors[monitor_name] = monitor_view

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


monitor = MonitoringRegistry()
