# -*- coding: utf-8 -*-
from django.forms import ModelForm
from django.core.exceptions import ValidationError
from models import *

class EnergyForm(ModelForm):
    class Meta:
        model=Energy
#        exclude=('date_time')
    def clean(self):
        last = Energy.objects.latest('date')
        cleaned_data = self.cleaned_data
        error={}
        errors=False
        for field in ['iwater','uwater','gaz']:
            if int(cleaned_data.get(field)) < getattr(last,field):
                error['energy-'+field]=u'Показания должны расти, а не уменьшатся ' +str(getattr(last,field))
                errors=True
        if errors:
            self._errors.update(error)
            raise ValidationError(u'В форме есть ошибки исправьте их')
        else:
            return cleaned_data


class TeploForm(ModelForm):
    class Meta:
        model=Teplo
  