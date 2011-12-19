# -*- coding: utf-8 -*-
from django.conf.urls.defaults import *
from piston.resource import Resource
from api.handlers import EnergyHandler

energy_resource = Resource(EnergyHandler)

urlpatterns = patterns('',
                       url(r'^energy/(?P<id>\d+)/$', energy_resource),
                       url(r'^energys/$', energy_resource),
                       )