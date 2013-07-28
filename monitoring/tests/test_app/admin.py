"""Admin classes for the test_app of the monitoring app."""
from django.contrib import admin

from .models import UserLoginCount


admin.site.register(UserLoginCount)
