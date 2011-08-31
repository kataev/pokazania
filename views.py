# -*- coding: utf-8 -*-
from django.http import HttpResponse
from django.template.loader import render_to_string
from django.shortcuts import render_to_response
from django.template import RequestContext
from cjson import encode as json
import datetime
import csv
from pokazania.teplo.models import *
from pokazania.energy.models import *
from dojango.util import dojo_collector

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


def delta(request,model):
    response = {'identifier':'id','items':[]}

    if True:

        a = model.objects.order_by('date').reverse()
        query = a[:len(a)-1]
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
                    vaw = round((getattr(next,f.name)-getattr(cur,f.name))/w,2)
                    if vaw < -1000:
                        vaw = 0
                    var.update({f.name:vaw})
            var['identity']=i+1
            response['items'].append(var)

    return HttpResponse(json(response),mimetype="application/json")

def main(request):
    forms = [energyForm(auto_id=False),teploForm(auto_id=False)]
    dojo_collector.add_module('dijit.Dialog')
    dojo_collector.add_module('dijit.layout.StackContainer')
    dojo_collector.add_module('dijit.form.Form')
    dojo_collector.add_module('dijit.form.HorizontalSlider')
    dojo_collector.add_module('dijit.layout.BorderContainer')
    dojo_collector.add_module('dijit.layout.TabContainer')
    dojo_collector.add_module('dijit.MenuBar')
    dojo_collector.add_module('dijit.MenuBarItem')
    dojo_collector.add_module('dijit.PopupMenuBarItem')
    dojo_collector.add_module("dojox.charting.widget.Chart2D")
    dojo_collector.add_module("dojox.charting.widget.Legend")
    dojo_collector.add_module("dojox.charting.themes.PlotKit.green")
    dojo_collector.add_module("dojox.charting.themes.Claro")
    dojo_collector.add_module("dojox.charting.DataSeries")
    dojo_collector.add_module("dojox.charting.widget.SelectableLegend")
    dojo_collector.add_module("dojox.charting.action2d.Tooltip")
    dojo_collector.add_module("dojo.date.locale")
#    dojo_collector.add_module("dojo.data.ItemFileReadStore")
    return render_to_response('main.html', {'forms':forms},context_instance=RequestContext(request))


def form(request):
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
