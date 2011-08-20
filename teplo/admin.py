# -*- coding: utf-8 -*-
from django.contrib import admin
from pokazania.teplo.models import *

class teploAdmin(admin.ModelAdmin):
    pass

admin.site.register(teplo, teploAdmin)
