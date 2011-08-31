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


class DayManager(models.Manager):
    def all(self,**kwargs):
        query = super(DayManager, self).all(**kwargs)
#        l = len(query)
        for q in query:
            try:
                next = q.get_previous_by_date()
                for field in q._meta.fields:
                    if field.name not in ['id','date','date_time']:
                        delta  = int((next.date - q.date).days)
#                        cur = getattr(q,field.name)
                        
                        setattr(q,field.name,round((getattr(next,field.name)-getattr(q,field.name))/delta,2))
            except q.DoesNotExist:
                pass
        return query
        

class energyDay(energy):
    class Meta:
        proxy = True
    objects = DayManager()

    


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