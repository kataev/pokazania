from django.conf.urls.defaults import patterns, include, url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.contrib import admin
admin.autodiscover()

from pokazania.energy.models import energy
from pokazania.teplo.models import teplo


urlpatterns = patterns('',
    # Examples:
     url(r'^excel/$', 'pokazania.views.excel', name='excel'),
     url(r'^last/$', 'pokazania.views.show_last', name='last'),
     url(r'^delta/energy/$', 'pokazania.views.delta',{'model':energy}, name='delta_energy'),
     url(r'^delta/teplo/$', 'pokazania.views.delta',{'model':teplo}, name='delta_teplo'),
     url(r'^$', 'views.main', name='main'),
     url(r'^form/$', 'pokazania.views.form', name='form'),
    # url(r'^pokazania/', include('pokazania.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    (r'^dojango/', include('dojango.urls')),
    url(r'^datagrid-list/(?P<app_name>.+)/(?P<model_name>.+)/$', 'dojango.views.datagrid_list', name="dojango-datagrid-list"),

)


urlpatterns += staticfiles_urlpatterns()

