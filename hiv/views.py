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
	if 'name' in request.POST and request.POST['name']:
		search = request.POST['name']
		results = Patient.objects.all()
		# First see if we have an exact match
		patients = results.filter(name__iexact=search)
		if not patients:
			# Expand the search to see any patients
			patients = results.filter(name__icontains=search)
		return render_to_response('hiv/patient_result_list.html',
						{'object_list':patients})
	else:
		form = PatientSearchForm()
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
	return create_update.create_object(
		request,
		form_class=VisitForm
	)

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
	return create_update.update_object(
		request,
		form_class=VisitForm,
		object_id = object_id
	)




###################### END: Visit Views #############################



