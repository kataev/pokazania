# -*- coding: utf-8 -*-
from django.db import models
from dojango.forms import ModelForm
from django.core.exceptions import ValidationError


class energy(models.Model):
    date_time=models.DateTimeField(u"Дата и время",auto_now=True)
    date=models.DateField(u"Дата")
    elec4=models.FloatField(u"Электр 4 ячейка")
    elec16=models.FloatField(u"Электр 16 ячейка")
    iwater=models.FloatField(u"Пром. Вода")
    uwater=models.FloatField(u"Хоз. Вода")
    gaz=models.PositiveIntegerField(u"Газ нм³")

    def __unicode__(self):
        return u'%s от %s' % (self._meta.verbose_name,str(self.date))



    
    def get_full_info(self):
        info = self.__dict__
        info.pop('_state')
        for a in info:
            if a in ['date','date_time']:
                info[a]=str(info[a])
            else:
                info[a]=float(info[a])
        return info

    class Meta():
        verbose_name = u"Энергоресурсы"
        verbose_name_plural = u"Энергоресурсы"
        ordering = ('-date',)

    class Admin:
        list_display = ('date','elec4','elec16','iwater','uwater','gaz')

class energyForm(ModelForm):
    @property
    def verbose_name(self):
        return self._meta.model._meta.verbose_name
    class Meta:
        model=energy
#        exclude=('date_time')
    def clean(self):
        last = energy.objects.latest('date')
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