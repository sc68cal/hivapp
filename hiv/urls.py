# To change this template, choose Tools | Templates
# and open the template in the editor.
from django.conf.urls.defaults import *
from hiv.views import *


urlpatterns = patterns('',
	# Example:
	# (r'^btech/', include('btech.foo.urls')),

	# Uncomment the admin/doc line below and add 'django.contrib.admindocs'
	# to INSTALLED_APPS to enable admin documentation:
	# (r'^admin/doc/', include('django.contrib.admindocs.urls')),

	(r'^crf/', ExistingCaseReportForm([
					PatientSelectForm,
					AlcoholForm,
					TobaccoForm,
					ExposureForm,
					HivForm,
					]),
				),
	(r'^newcrf/',NewCaseReportForm([PatientFirstVisitForm,AlcoholForm,TobaccoForm,
					   ExposureForm,HivForm])),
	(r'^mutation/(?P<object_id>\d+)/$',mutation_detail),
	(r'^patient/$',patient_list),
	(r'^patient/(?P<object_id>\d+)/$',patient_detail),
	(r'^patient/add/$',patient_create),
	(r'^patient/edit/(?P<object_id>\d+)/$',patient_update),
	(r'^search/$',patient_search),
	(r'^visit/$',visit_list),
	(r'^visit/(?P<object_id>\d+)/$',visit_detail),

	(r'^visit/add/$',visit_create),
	(r'^visit/edit/(?P<object_id>\d+)/$',visit_update),
	(r'^api/json/patient/$',ajax_patient_list),
	(r'^$', index)
)



