from django.conf.urls.defaults import *
from helix.hiv.views import *
from django.contrib.auth.views import login,logout
from django.contrib import databrowse
from helix import settings

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
	# Example:
	# (r'^btech/', include('btech.foo.urls')),

	# Uncomment the admin/doc line below and add 'django.contrib.admindocs'
	# to INSTALLED_APPS to enable admin documentation:
	# (r'^admin/doc/', include('django.contrib.admindocs.urls')),

	(r'^accounts/login/$', login),
	(r'^accounts/logout/$',logout),
	(r'^admin/', include(admin.site.urls)),
	(r'^mutation/(?P<object_id>\d+)/$',mutation_detail),
	(r'^patient/$',patient_list),
	(r'^patient/(?P<object_id>\d+)/$',patient_detail),
	(r'^patient/add$',patient_create),
	(r'^patient/edit/(?P<object_id>\d+)/$',patient_update),
	(r'^search/$',patient_search),
	(r'^visit/$',visit_list),
	(r'^visit/(?P<object_id>\d+)/$',visit_detail),

	(r'^visit/add$',visit_create),
	(r'^visit/edit/(?P<object_id>\d+)/$',visit_update),
	(r'^$', index)
)

if settings.DEBUG:
	urlpatterns += patterns('',
	(r'^site_media/(?P<path>.*)$', 'django.views.static.serve',
		{'document_root':
		'/Users/scollins/Programming/CoreITPro/BTech/helix/media/'}),
	(r'^databrowse/(.*)', databrowse.site.root),
)


## Databrowse
if settings.DEBUG:
	databrowse.site.register(Patient)
	databrowse.site.register(Visit)
