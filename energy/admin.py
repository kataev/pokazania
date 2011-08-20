from django.contrib import admin
from pokazania.energy.models import *

class energyAdmin(admin.ModelAdmin):
    pass

admin.site.register(energy, energyAdmin)
