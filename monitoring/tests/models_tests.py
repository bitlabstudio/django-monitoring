"""Tests for the models of the monitoring app."""
from django.test import TestCase

from ..models import MonitoringBase
from .test_app.models import SomeCount


class MonitoringBaseTestCase(TestCase):
    """Tests for the ``MonitoringBase`` base class."""
    longMessage = True

    def test_add(self):
        """Should throw ``NotImplementedError``."""
        self.assertRaises(NotImplementedError, MonitoringBase.add)


class IntegerCountBaseTestCase(TestCase):
    """Tests for the ``IntegerCountBase`` model."""
    longMessage = True

    def test_add(self):
        SomeCount.add(1)
        self.assertEqual(SomeCount.objects.all().count(), 1, msg=(
            'When calling add it should add one new data item to the table'))
