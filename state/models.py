# -*- coding: utf-8 -*-
from django.db import models

class Energy(models.Model):
    date_time=models.DateTimeField(u"Дата и время",auto_now=True)
    date=models.DateField(u"Дата")
    elec4=models.FloatField(u"Электр 4 ячейка")
    elec16=models.FloatField(u"Электр 16 ячейка")
    iwater=models.FloatField(u"Пром. Вода")
    uwater=models.FloatField(u"Хоз. Вода")
    gaz=models.PositiveIntegerField(u"Газ нм³")

    def to_dict(self):
        return dict(udate= self.udate(), elec4=self.elec4, elec16=self.elec16,
                    iwater = self.iwater, uwater=self.uwater, gaz=self.gaz)

    def udate(self):
        return int(self.date.strftime('%s'))*1000

    def __unicode__(self):
        return u'%s от %s' % (self._meta.verbose_name,str(self.date))

    class Meta():
        verbose_name = u"Энергоресурсы"
        verbose_name_plural = u"Энергоресурсы"
        ordering = ('-date',)

class Teplo(models.Model):
    date_time=models.DateTimeField(u"Дата и время",auto_now=True)
    date=models.DateField(u"Дата")
    henergy=models.FloatField(u"ТЭнергия кал")
    hot_water=models.FloatField(u"Расход гор.воды м³")
    rpr=models.FloatField(u"Давл прих кг/см²")
    robr=models.FloatField(u"Давл уход кг/см²")
    tpr=models.FloatField(u"Темп прих С°")
    tobr=models.FloatField(u"Темп обр С°")

    class Meta():
        verbose_name = u"Тепло"
        verbose_name_plural = u'Тепло'
        ordering = ('-date',)

    def __unicode__(self):
        return u'%s от %s' % (self._meta.verbose_name,str(self.date))





