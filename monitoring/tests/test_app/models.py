"""Models for testing the abstract base classes of the monitoring app."""
from django.db import models

from monitoring.models import IntegerCountBase


class UserCount(IntegerCountBase):
    pass
