# -*- coding: utf-8 -*-

from alerts.models import Alert, AlertMatch
from django.contrib import admin

admin.site.register(Alert)
admin.site.register(AlertMatch)
