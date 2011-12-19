# -*- coding: utf-8 -*-
from piston.handler import BaseHandler
from state.models import Energy

class EnergyHandler(BaseHandler):
    model = Energy
    fields = ('id', 'udate','elec4','elec16','iwater','uwater','gaz')

    def asd(self):
        return 12