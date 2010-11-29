# $Id$
from django.shortcuts import render_to_response,get_object_or_404
from hiv.models import *
from hiv.forms import *
from django.views.generic import list_detail,create_update
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.core.urlresolvers import reverse
try:
	import json
except ImportError:
	import simplejson as json

def index(request):
	return render_to_response('hiv/base.html')

###################### BEGIN: Mutation Views #############################
@login_required
def mutation_create(request):
	return create_update.create_object(
		request,
		model=Mutation
	)


@login_required
def mutation_detail(request,object_id):
	mutation = get_object_or_404(Mutation,pk=object_id)
	return list_detail.object_detail(
		request,
		queryset=Mutation.objects.all(),
		object_id = mutation.id

	)

@login_required
def mutation_update(request,object_id):
	return create_update.update_object(
		request,
		model=Mutation,
		object_id = object_id
	)


###################### END: Mutation Views #############################

################### BEGIN: Patient Views #############################

@login_required
def ajax_patient_list(request):
	json_data = {}
	json_data['page'] = request.POST['page'];
	json_data['rows'] = []

	count = int(request.POST['rp'])
	if request.POST['sortname'] == 'patient_id':
		if request.POST['sortorder'] == 'asc':
			results = Patient.objects.order_by('patient_id')
		else:
			results = Patient.objects.order_by('-patient_id')
	if request.POST['page'] == 1:
		start = 0
	else:
		start = (int(request.POST['page'])-1) * int(request.POST['rp'])
	end = start + count
	if request.POST['qtype'] == 'name':
		results = results.filter(patient_id__contains=request.POST['query'])
	elif request.POST['qtype'] =='dob':
		results = results.filter(year_of_birth=request.POST['query'])
	elif request.POST['qtype'] == 'gender':
		results = results.filter(gender=request.POST['query'])
	elif request.POST['qtype'] == 'sero':
		results = results.filter(sero_positive_since=request.POST['query'])
	for patient in results[start:end]:
		row = {'id':patient.id,'cell':[]}
		# number of visits
		row['cell'].append("<a href=" + reverse(patient_detail,args=[patient.id])+">"+patient.patient_id+"</a>")
		row['cell'].append(patient.gender)
		row['cell'].append(patient.year_of_birth)
		row['cell'].append(patient.visit_set.count())
		json_data['rows'].append(row)
	json_data['total'] = results.count()
	return HttpResponse(json.dumps(json_data)) 
		

@login_required
def patient_create(request):
	return create_update.create_object(
		request,
		form_class=PatientForm
	)

@login_required
def patient_detail(request,object_id):
	patient = get_object_or_404(Patient,pk=object_id)
	return list_detail.object_detail(
		request,
		queryset=Patient.objects.all(),
		object_id = patient.id
	
	)

@login_required
def patient_list(request):
	return render_to_response('hiv/patient_list.html')

@login_required
def patient_search(request):
	# Search by patient name
	if request.POST:
		results = Patient.objects.all()
		if 'patient_id' in request.POST and request.POST['patient_id']:
			search = request.POST['patient_id']
			# First see if we have an exact match
			results = results.filter(patient_id__iexact=search)
			if not results:
				# Expand the search to see any patients
				patients = results.filter(patient_id__icontains=search)
		if 'gender' in request.POST and request.POST['gender']:
			results = results.filter(gender=request.POST['gender'])
		if 'year_of_birth' in request.POST and request.POST['year_of_birth']:
			results = results.filter(year_of_birth=request.POST['year_of_birth'])
		if 'sero_positive_since' in request.POST and request.POST['sero_positive_since']:
			results = results.filter(sero_positive_since=request.POST['sero_positive_since'])
		return render_to_response('hiv/patient_result_list.html',
						{'object_list':results})
	else:
		form = PatientForm()
		return render_to_response("hiv/patient_form.html", 
							{"form":form})

@login_required
def patient_update(request,object_id):
	return create_update.update_object(
		request,
		form_class=PatientForm,
		object_id = object_id,
	)


###################### END: Patient Views #############################



###################### BEGIN: Visit Views #############################
@login_required
def ajax_visit_list(request):
	json_data = {}
	json_data['page'] = request.POST['page'];
	json_data['rows'] = []
	count = int(request.POST['rp'])
	if request.POST['page'] == 1:
		start = 0
	else:
		start = (int(request.POST['page'])-1) * int(request.POST['rp'])
	json_data['rows'] = []
	end = start + count
	if request.POST['sortname'] == 'name':
		if request.POST['sortorder'] == 'asc':
			results = Visit.objects.order_by('name')
		else:
			results = Patient.objects.order_by('-name')
	elif request.POST['sortname'] == 'date':
		if request.POST['sortorder'] == "asc":
			results = Visit.objects.order_by('date')
		else:
			results = Visit.objects.order_by('-date')
	elif request.POST['sortname'] == 'cd4':
		if request.POST['sortorder'] == "asc":
			results = Visit.objects.order_by('cd4')
		else:
			results = Visit.objects.order_by('-cd4')
	elif request.POST['sortname'] == 'viral':
		if request.POST['sortorder'] == 'asc':
			results = Visit.objects.order_by('viral')
		else:
			results = Visit.objects.order_by('-viral')
	elif request.POST['sortname'] == 'dsg':
		if request.POST['sortorder'] == 'asc':
			results = Visit.objects.order_by('dsg')
		else:
			results = Visit.objects.order_by('-dsg')
	for visit in results[start:end]:
		row = {'id':visit.id,'cell':[]}
		row['cell'].append("<a href=" + reverse(visit_detail,args=[visit.id])+">"+visit.name+"</a>")
		row['cell'].append(visit.date)
		row['cell'].append(visit.cd4)
		row['cell'].append(visit.viral)
		row['cell'].append(visit.dsg)
		json_data['rows'].append(row)
	json_data['total'] = results.count()
	return HttpResponse(json.dumps(json_data)) 

@login_required
def visit_create(request):
	if not request.POST:
		return create_update.create_object(
			request,
			form_class=VisitForm
		)
	else:
		form = VisitForm(request.POST)
		form.save()
		return render_to_response('hiv/base.html')


@login_required
def visit_detail(request,object_id):
	visit = get_object_or_404(Visit,pk=object_id)
	return list_detail.object_detail(
		request,
		queryset=Visit.objects.all(),
		object_id = visit.id
	
	)


@login_required
def visit_list(request):
	return render_to_response('hiv/visit_list.html')



@login_required
def visit_update(request,object_id):
	if not request.POST:
		return create_update.update_object(
			request,
			form_class=VisitForm,
			object_id = object_id
		)
	else:
		form = VisitForm(postdata=request.POST,visit_id=object_id)
		form.save()
		return render_to_response('hiv/base.html')

###################### END: Visit Views #############################



