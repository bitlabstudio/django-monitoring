Django Monitoring
============

A reusable Django app to monitor all aspects of your webapp

Installation
------------

To get the latest stable release from PyPi

.. code-block:: bash

    $ pip install django-monitoring

To get the latest commit from GitHub

.. code-block:: bash

    $ pip install -e git+git://github.com/bitmazk/django-monitoring.git#egg=monitoring

TODO: Describe further installation steps (edit / remove the examples below):

Add ``monitoring`` to your ``INSTALLED_APPS``

.. code-block:: python

    INSTALLED_APPS = (
        ...,
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
