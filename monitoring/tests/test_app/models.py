"""Models for testing the abstract base classes of the monitoring app."""
from django.contrib.auth.signals import user_logged_in
from django.dispatch import receiver

from monitoring import monitor
from monitoring.models import IntegerCountBase
from monitoring.views import IntegerCountView


MONITOR_USER_LOGIN_COUNT = 'user_login_count'


class UserLoginCount(IntegerCountBase):
    pass


monitor.register(
    MONITOR_USER_LOGIN_COUNT,
    IntegerCountView.as_view(
        model=UserLoginCount,
    ))


@receiver(user_logged_in)
def user_logged_in_handler(sender, *args, **kwargs):
    monitor.get(MONITOR_USER_LOGIN_COUNT).add(1)
