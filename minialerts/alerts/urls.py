# -*- coding: utf-8 -*-

from django.conf.urls import patterns, include, url

urlpatterns = patterns('alerts.views',
    url(r'^$', 'index'),
    url(r'list/?$', 'index', name="alerts_list"),
    url(r'push/?$', 'push'),
    url(r'toggledone/(\d+)/$', 'toggledone'),
    url(r'toggleignore/(\d+)/$', 'toggleignore'),
)
