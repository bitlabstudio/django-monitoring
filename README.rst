Django Monitoring
=================

DO NOT USE THIS. Work in progress.

A reusable Django app to monitor all aspects of your webapp.

The idea is to create an app that provides some APIs that can be re-used
by any other app.

Let's say you want to create a graph that shows how many users sign up at your
site every day.

First you will create a model that can hold this data. django-monitoring will
provide some abstract base classes for commonly used model types::

    class MonitorUserCount(IntegerCountBase, models.Model):
        pass

Next you will register a new monitor that is connected to that monitor model.
This is similar to registering model admins, we need to do this so that the
monitoring view knows which snippets to display::

    from monitoring import monitor
    from monitoring.views import IntegerCountView
    from myapp.models import MonitorUserCount

    monitor.register(
        'user_count', IntegerCountView.as_view(model=MonitorUserCount))

Now you can add a data point to this monitor anywhere in your code::

    from monitoring import monitor

    def post_registration__handler(sender, user, *args, **kwargs):
        monitor.get('user_count').add(1)

django-monitoring will figure out, that the ``user_count`` monitor is connected
to the ``MonitorUserCount`` model and it will also know that this model is
of the type ``MonitorCountBase`` which will know how to add one data point to
itself. In this case it would just add a row to the table which says that 1
user was added at ``timezone.now()``.

Finally django-monitoring provides a view which will show graphs for all
connected monitors. I still have to think about how to teach that view which
monitors to show, how to render the data and how to filter the data.

The base classes will probably have an attribute which describes the default
template but you could easily override those templates for your app.

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

Add jQuery and ``monitoring.js`` at the bottom of your ``base.html``::

.. code-block:: html

    <script src="//ajax.googleapis.com/ajax/libs/jquery/1.7.0/jquery.min.js"></script>
    <script src="{{ STATIC_URL }}monitoring/js/monitoring.js"></script>


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
