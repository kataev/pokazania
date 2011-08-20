# -*- coding: utf-8 -*-
from django.db import models
from dojango.forms import ModelForm
from django.core.exceptions import ValidationError

class teplo(models.Model):
    date_time=models.DateTimeField(u"Дата и время",auto_now=True)
    date=models.DateField(u"Дата")
    henergy=models.FloatField(u"ТЭнергия кал")
    hot_water=models.FloatField(u"Расход гор.воды м³")
    rpr=models.FloatField(u"Давл прих кг/см²")
    robr=models.FloatField(u"Давл уход кг/см²")
    tpr=models.FloatField(u"Темп прих С°")
    tobr=models.FloatField(u"Темп обр С°")
    def get_full_info(self):
        info = self.__dict__
        info.pop('_state')
        for a in info:
            if a in ['date','date_time']:
                info[a]=str(info[a])
            else:
                info[a]=float(info[a])
        return info

    def name(self):
        return self.date_time

    class Meta():
        verbose_name = u"Тепло"
        verbose_name_plural = u'Тепло'
        ordering = ('-date',)

    class Admin():
        list_display = ('date', 'henergy', 'hot_water', 'rpr','robr','tpr','tobr')

    def __unicode__(self):
        return u'%s от %s' % (self._meta.verbose_name,str(self.date))



class teploForm(ModelForm):
    @property
    def verbose_name(self):
        return self._meta.model._meta.verbose_name

    class Meta:
        model=teplo


