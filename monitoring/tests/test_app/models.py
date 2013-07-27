"""Models for testing the abstract base classes of the monitoring app."""
from django.db import models

from ...models import IntegerCountBase


class SomeCount(IntegerCountBase):
    pass
