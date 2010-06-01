# $Id$
from django.shortcuts import render_to_response,get_object_or_404
from helix.hiv.models import *
from helix.hiv.forms import *
from django.views.generic import list_detail,create_update
from django.contrib.auth.decorators import login_required


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
	return list_detail.object_list(
		request,
		queryset=Patient.objects.all()
	)

@login_required
def patient_search(request):
	# Search by patient name
	if 'patient_id' in request.POST and request.POST['patient_id']:
		search = request.POST['patient_id']
		results = Patient.objects.all()
		# First see if we have an exact match
		patients = results.filter(patient_id__iexact=search)
		if not patients:
			# Expand the search to see any patients
			patients = results.filter(patient_id__icontains=search)
		return render_to_response('hiv/patient_result_list.html',
						{'object_list':patients})
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
	return list_detail.object_list(
		request,
		queryset=Visit.objects.all()
	)


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



