import *

def show_form(request):
    from pokazania.accounting.models import teploForm
    from pokazania.accounting.models import EnergyForm 
    from django.template.loader import render_to_string
    #temp = loader('form.html')
    teplo = teploForm(prefix="teplo")
    energy= EnergyForm(prefix="energy")
    re=render_to_string('form.html',{'form':{'teplo':teplo.as_ul(),'energy':energy.as_ul()}})
    return HttpResponse(re,mimetype="text/html")

def show_main(request):
    
    from django.template.loader import render_to_string
    re=render_to_string('main.html')
    return HttpResponse(re,mimetype="text/html")

def excell(request):
    from pokazania.accounting.models import *
    response = HttpResponse(mimetype='text/csv')
    
    response['Content-Disposition'] = 'attachment; filename=%s.csv' % datetime.datetime.now()
    
    ver = []
    for a in teplo._meta.fields:
        ver.append(a.verbose_name.encode('utf-8'))
    writer = csv.writer(response,delimiter=';')
    writer.writerow([teplo._meta.verbose_name.encode("utf-8")])
    writer.writerow(ver)
    for a in teplo.objects.values_list().all():
        writer.writerow(a)

    ver = []
    for a in Energy._meta.fields:
        ver.append(a.verbose_name.encode('utf-8'))
    writer = csv.writer(response,delimiter=';')
    writer.writerow([Energy._meta.verbose_name.encode("utf-8")])
    writer.writerow(ver)
    for a in Energy.objects.values_list().all():
        writer.writerow(a)

    return response

def show_last(request,year,month,**kwargs):
    date=datetime.datetime(int(year),int(month),1,0,0)
    response = {'teplo':{'identifier':'id','date':'name','items':[]},'energy':{'identifier':'id','label':'name','items':[]}}
    for a in teplo.objects.filter(date_time__gte=date):
        response['teplo']['items'].append(a.get_full_info())
    for a in energy.objects.filter(date_time__gte=date):
        response['teplo']['items'].append(a.get_full_info())

    q = {'store':{'identifier':'id','label':'name','items':[]}}
    return HttpResponse(json.encode(q),mimetype="application/json")

def show_info(request):
    from pokazania.accounting.models import teplo,Energy
    re = {'teplo':teplo.objects.latest('id').get_full_info()}
    re['energy']=Energy.objects.latest('id').get_full_info()
    return HttpResponse(json.encode(re),mimetype="application/json")

def add(request,oper):

    if oper=='teplo':
        from pokazania.accounting.models import teploForm as f
    if oper=='energy':
        from pokazania.accounting.models import EnergyForm as f
    
    if request.method == 'GET':
        return HttpResponse(json.encode({'status':'error','message':u'Метод GET не рабоатет'}),mimetype="application/json")

    if request.method == 'POST':
        post=request.POST.copy()
        for a in post:
            post[a]=post[a].replace(',','.')
        data = f(post)
        if data.is_valid():        
            re = data.save()
            return HttpResponseRedirect('../../show/%s/%s/' % (oper,re.id))
        else:
            re = {}
            re['status']='error'
            re['message']=data.errors
            return HttpResponse(json.encode(re),mimetype="application/json")

from django.db import models
from dojango.forms import ModelForm

class teplo(models.Model):
    date_time=models.DateTimeField(u"Дата и время",auto_now=True)
    date=models.DateField(u"Дата",auto_now=False)
    henergy=models.FloatField(u"ТеплоЭнергия гкал")
    hot_water=models.FloatField(u"Расход горячей воды м³")
    rpr=models.FloatField(u"Давл приходящее кг/см²")
    robr=models.FloatField(u"Давл уходящее кг/см²")
    tpr=models.FloatField(u"Темп приходящая С°")
    tobr=models.FloatField(u"Темп обратная С°")
    def get_full_info(self):
        info = self.__dict__
        info.pop('_state')
        for a in info:
            info[a]=str(info[a])
        return info
    class Meta():
        verbose_name = u"Тепло"
    
        
    
class energy(models.Model):
    date_time=models.DateTimeField(u"Дата и время",auto_now=True)
    date=models.DateField(u"Дата",auto_now=False)
    elec4=models.FloatField(u"Электр 4 ичейка")
    elec16=models.FloatField(u"Электр 16 ичейка")
    iwater=models.FloatField(u"Пром. Вода")
    uwater=models.FloatField(u"Хоз. Вода")
    gaz=models.IntegerField(u"Газ нм³",max_length=60) 
    def get_full_info(self):
        info = self.__dict__
        info.pop('_state')
        for a in info:
            info[a]=str(info[a])
        return info
    
    class Meta():
        verbose_name = u"Энергоресурсы"    
    
#~ class gaz(models.Model):
    #~ date_time=models.DateTimeField(auto_now=True)
    #~ total=models.DecimalField(u"Газ",max_digits=12, decimal_places=2)


class teploForm(ModelForm):
    class Meta:
        model=teplo
        #exclude=('date_time')
        
class EnergyForm(ModelForm):
    class Meta:
        model=energy
        #exclude=('date_time')
