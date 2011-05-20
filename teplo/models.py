# -*- coding: utf-8 -*-
from django.db import models
from dojango.forms import ModelForm

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
    class Meta():
        verbose_name = u"Тепло"



class teploForm(ModelForm):
    class Meta:
        model=teplo
#        exclude=('date_time')