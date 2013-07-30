"""Models and base classes for the monitoring app."""
from django.db import models
from django.utils.translation import ugettext_lazy as _


class MonitoringBase(object):
    """
    Abstract base class for all monitoring related model classes.

    This class will define all verbs that we can do with our various monitoring
    classes. If someone tries to call ``monitor.get('name').remove()`` but
    that verb has not been implemented for that specific monitor, we will
    raise ``NotImplementedError``.

    """
    @staticmethod
    def add(*args, **kwargs):
        """Adds a data point to the table."""
        raise NotImplementedError


class IntegerCountBase(MonitoringBase, models.Model):
    """
    Counts that something has happened at a certain date and time.

    :value: Integer representing the amount of events that happend.
      Usually this would be 1, for example when 1 new user registers.
    :date_created: Datetime when this event happened.

    """
    value = models.IntegerField(
        verbose_name=_('Value'),
    )

    datetime_created = models.DateTimeField(
        verbose_name=_('DateTime created'),
        auto_now_add=True,
    )

    date_created = models.DateField(
        verbose_name=_('Date created'),
        auto_now_add=True,
    )

    class Meta:
        abstract = True
        ordering = ('-date_created', )

    def __unicode__(self):
        return '{0} at {1}'.format(self.value, self.date_created)

    @classmethod
    def add(cls, value):
        cls.objects.create(value=value)
