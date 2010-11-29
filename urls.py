# $Id$
from django.conf.urls.defaults import *
from django.contrib import databrowse
from hiv.models import Patient,Visit
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
	(r'',include('hiv.urls')),
	(r'^accounts/login/$', "django.contrib.auth.views.login"),
	(r'^accounts/logout/$','django.contrib.auth.views.logout',{'next_page':settings.LOGIN_URL}),
	(r'^accounts/password','django.contrib.auth.views.password_change',{'post_change_redirect':settings.LOGIN_REDIRECT_URL}),
	(r'^admin/', include(admin.site.urls)),

)

if settings.DEBUG:
	urlpatterns += patterns('',
	(r'^site_media/(?P<path>.*)$', 'django.views.static.serve',
		{'document_root':
		'/Users/scollins/Programming/CoreITPro/BTech/hivapp/helix/media/'}),
	(r'^databrowse/(.*)', databrowse.site.root),
	)


## Databrowse
if settings.DEBUG:
	databrowse.site.register(Patient)
	databrowse.site.register(Visit)
