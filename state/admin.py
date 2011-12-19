# -*- coding: utf-8 -*-
from django.contrib import admin
from models import *


class EnergyAdmin(admin.ModelAdmin):
    list_display = ('date','elec4','elec16','iwater','uwater','gaz')

class TeploAdmin(admin.ModelAdmin):
    list_display = ('date', 'henergy', 'hot_water', 'rpr','robr','tpr','tobr')

admin.site.register(Energy,EnergyAdmin)
admin.site.register(Teplo,TeploAdmin)