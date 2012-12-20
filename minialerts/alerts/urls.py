# -*- coding: utf-8 -*-

from django.conf.urls import patterns, include, url

urlpatterns = patterns('alerts.views',
    url(r'^$', 'index'),
    url(r'list/?$', 'index'),
    url(r'push/?$', 'push'),
    url(r'toggle/(\d+)/$', 'toggle', name="toggle"),
)
