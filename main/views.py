# -*- coding: utf-8 -*-
from django.http import HttpResponse
from django.template.loader import render_to_string
from cjson import encode as json
import datetime
import csv
from pokazania.teplo.models import *
from pokazania.energy.models import *

def excel(request):
    response = HttpResponse(mimetype='text/csv')
    q = [teplo,energy]
    response['Content-Disposition'] = 'attachment; filename=%s.csv' % datetime.datetime.now()

    for model in q:
        ver = []
        for a in model._meta.fields:
            ver.append(a.verbose_name.encode('utf-8'))
        writer = csv.writer(response,delimiter=';')
        writer.writerow([model._meta.verbose_name.encode("utf-8")])
        writer.writerow(ver)
        for a in model.objects.values_list().all():
            writer.writerow(a)
    
    return response

def show_last(request,**kwargs):
    date=datetime.datetime(int(2011),int(5),1,0,0)
    response = {'teplo':{'identifier':'id','items':[],'fields':[]},'energy':{'identifier':'id','items':[],'fields':[]}}
    q=[teplo,energy]
    for model in q:
        query = model.objects.order_by('date').reverse()[:31]
        l = len(query)
        fields = model._meta.fields
        for i in range(l-1):
            cur = query[i]
            var = {}
            for f in fields:
                if f.name =='id':
                    var.update({'id':cur.pk})
                    continue
                if f.name in ['date','date_time']:
                    var.update({f.name:str(getattr(cur,f.name))})
                else:
                    var.update({f.name:round(getattr(cur,f.name),2)})
            var['identity']=i+1
            response[model._meta.app_label]['items'].append(var)
        for f in fields:
            if f.name in ['date_time','id']:
                continue
            if f.name in ['date','date_time']:
                response[model._meta.app_label]['fields'].append({
                    'field': f.name,
                    'name': f.verbose_name,
                    'width': 'auto'})
            else:
                response[model._meta.app_label]['fields'].append({
                    'field': f.name,
                    'name': f.verbose_name,
                    'width': '200px'})


    return HttpResponse(json(response),mimetype="application/json;charset=utf-8;")


def delta(request,**kwargs):
    response = {'teplo':{'identifier':'id','items':[],'fields':[]},'energy':{'identifier':'id','items':[],'fields':[]}}
    q = [teplo,energy]

    for model in q:
        query = model.objects.order_by('date').reverse()[:31]
        l = len(query)
        fields = model._meta.fields
        for i in range(l-1):
            cur = query[i]
            next = query[i+1]
            w = 1
            w = int((next.date - cur.date).days)
            if w == 0:
                w=1
            var = {}
            for f in fields:
                if f.name =='id':
                    var.update({'id':cur.pk})
                    continue
                if f.name in ['rpr','robr','tpr','tobr']:
                    var.update({f.name:round(getattr(cur,f.name),2)})
                    continue
                if f.name =='henergy':
                    var.update({f.name:round((getattr(next,f.name)-getattr(cur,f.name))*1000/w,2)})
                    continue
                if f.name in ['date','date_time']:
                    var.update({f.name:str(getattr(cur,f.name))})
                else:
                    var.update({f.name:round((getattr(next,f.name)-getattr(cur,f.name))/w,2)})
            var['identity']=i+1
            response[model._meta.app_label]['items'].append(var)
        for f in fields:
            if f.name in ['date_time','id']:
                continue
            if f.name in ['date','date_time']:
                response[model._meta.app_label]['fields'].append({
                    'field': f.name,
                    'name': f.verbose_name,
                    'width': 'auto'})
            else:
                response[model._meta.app_label]['fields'].append({
                    'field': f.name,
                    'name': f.verbose_name,
                    'width': '200px'})

    return HttpResponse(json(response),mimetype="application/json")

def main(response):
    rendered = render_to_string('main.html',{})
    return HttpResponse(rendered,mimetype="text/html;charset=utf-8")


def form(response):
    rendered = render_to_string('form.html',{'energy_form':energyForm().as_ul(),'teplo_form':teploForm().as_ul()})
    return HttpResponse(rendered,mimetype="text/html;charset=utf-8")


def form(request):

    models={'teplo':teplo,'energy':energy,'teploForm':teploForm,'energyForm':energyForm}
    
    if request.method == 'POST': # Если пост то обрабатываем данные
        post=request.POST.copy() # Копируем массив, ибо request - read only
        f=models[post['oper']+'Form']

        for field in post:
            post[field]=post[field].replace(',','.')

        form = f(post,prefix=post['oper'])

        if form.is_valid():
            inst = form.save()
            return HttpResponse(json({'status':'ok'}),mimetype="application/json;charset=utf-8")
        else:
            del form.errors['__all__']
            return HttpResponse(json({'status':'error','message':form.errors}),mimetype="application/json;charset=utf-8")
    else:
        rendered = render_to_string('form.html',{'energy_form':energyForm(prefix='energy').as_ul(),'teplo_form':teploForm(prefix='teplo').as_ul()})
        return HttpResponse(rendered,mimetype="text/html;charset=utf-8;")
