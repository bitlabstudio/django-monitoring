Django Monitoring
=================

**ATTENTION: Work in progress. APIs might change any time, but we are using it in 
production now so changes should not be too invasive.**

.. image:: https://raw.github.com/bitmazk/django-monitoring/master/monitor.png

A reusable Django app to monitor all aspects of your webapp.

The idea is to create an app that provides some APIs that can be re-used
by any other app. It is a bit similar to the Django admin: You register
monitors and tell the system three things:

1. The name of the monitor
2. The view that renders the data for the monitor
3. The modle that holds the data for the monitor

This app provides some default views and models for commonly used use cases but
if you have some really complex data that needs extensive computation and a
complicated chart to render, you can override anything to your liking.

Once you have registered all your monitors, you can go to a URL
``/monitoring/`` and see all your charts popping up via AJAX calls. We will
extend this gradually so that you can change the order of the charts or group
them into categories because if you have a lot of charts, it will probably be
quite slow to load them all all the time.

In your code, adding data points to your registered monitors works similar to
the logging module::

    from monitoring.register import monitor

    def some_method():
        # a user logs in
        monitor.get('user_login_count').add(1)

Vision
------

Let's say you want to create a graph that shows how many users sign up at your
site every day.

First you will create a model that can hold this data. django-monitoring will
provide some abstract base classes for commonly used model types::

    class MonitorUserCount(IntegerCountBase, models.Model):
        pass

Next you will register a new monitor that is connected to that monitor model.
This is similar to registering model admins, we need to do this so that the
monitoring view knows which snippets to display::

    from monitoring.register import monitor
    from monitoring.views import IntegerCountView
    from myapp.models import MonitorUserCount

    monitor.register(
        'user_count', IntegerCountView.as_view(model=MonitorUserCount))

Now you can add a data point to this monitor anywhere in your code::

    from monitoring.register import monitor

    def post_registration__handler(sender, user, *args, **kwargs):
        monitor.get('user_count').add(1)

django-monitoring will figure out, that the ``user_count`` monitor is connected
to the ``MonitorUserCount`` model and it will also know that this model is
of the type ``MonitorCountBase`` which will know how to add one data point to
itself. In this case it would just add a row to the table which says that 1
user was added at ``timezone.now()``.

Installation
------------

To get the latest stable release from PyPi (not yet released!)

.. code-block:: bash

    $ pip install django-monitoring

To get the latest commit from GitHub

.. code-block:: bash

    $ pip install -e git+git://github.com/bitmazk/django-monitoring.git#egg=monitoring

Add ``monitoring`` to your ``INSTALLED_APPS``

.. code-block:: python

    INSTALLED_APPS = (
        ...,
        'django_libs',
        'monitoring',
    )

Add the ``monitoring`` URLs to your ``urls.py``

.. code-block:: python

    urlpatterns = patterns('',
        ...
        url(r'^monitoring/', include('monitoring.urls')),
    )

Don't forget to migrate your database

.. code-block:: bash

    ./manage.py migrate monitoring

Add jQuery, YUI and ``monitoring.js`` at the bottom of your ``base.html``::

.. code-block:: guess

    <script src="//ajax.googleapis.com/ajax/libs/jquery/2.0.2/jquery.min.js"></script>
    <script src="//yui.yahooapis.com/3.11.0/build/yui/yui-min.js"></script>
    <script src="{{ STATIC_URL }}monitoring/js/monitoring.js"></script>

Make sure that you have a ``{% block main %}{% endblock %} in your
``base.html``.


Usage
-----

TODO: Describe usage or point to docs. Also describe available settings and
templatetags.


Contribute
----------

If you want to contribute to this project, please perform the following steps

.. code-block:: bash

    # Fork this repository
    # Clone your fork
    $ mkvirtualenv -p python2.7 django-monitoring
    $ python setup.py install
    $ pip install -r dev_requirements.txt

    $ git co -b feature_branch master
    # Implement your feature and tests
    $ git add . && git commit
    $ git push -u origin feature_branch
    # Send us a pull request for your feature branch
