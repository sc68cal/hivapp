# $Id$
from django.forms import ModelForm, Form
from django import forms
from helix.hiv.models import *
from django.contrib.formtools.wizard import FormWizard

class AlcoholForm(Form):
	current_use = forms.CharField(widget=forms.Select(choices=
						(
							("Yes","Yes"),
							("No","No"),
							("Never","Never"),
							("In The Past","In The Past")
						)
				   )
				   )
	beer_frequency = forms.IntegerField(required=False)
	wine_frequency = forms.IntegerField(required=False)
	liquor_frequency = forms.IntegerField(required=False)
	beer_date_if_stopped = forms.IntegerField(required=False)
	wine_date_if_stopped = forms.IntegerField(required=False)
	liquor_date_if_stopped = forms.IntegerField(required=False)

class DrugForm(ModelForm):
	class Meta:
		model = DrugUsed

class HivForm(Form):
	pass

class TobaccoForm(Form):
	current_use = forms.CharField(widget=forms.Select(choices=
					(
						("Yes","Yes"),
						("No","No"),
						("Never","Never"),
						("In The Past","In The Past")
					)
				)
				)
	type = forms.MultipleChoiceField(choices=
						(
							("Cigarettes","Cigarettes"),
							("Cigars","Cigars"),
							("Pipes","Pipes"),
							("Chewing Tobacco","Chewing Tobacco")

						)
					 ,required=False)
	frequency = forms.IntegerField(required=False)
	years_used = forms.IntegerField(required=False)

class ExposureForm(Form):
	exposures = forms.MultipleChoiceField(
						choices = [
								[a.pk,a.name]
								for a in Exposure.objects.all()
							  ]
					     )


# TODO: Create race table and do a ManyToMany foreign key?
class PatientForm(ModelForm):
	class Meta:
		model = Patient
	gender_choices = (
				("M","M"),
				("F","F"),
				("Transgender M->F","Transgender M->F"),
				("Transgender F->M","Transgender F->M"),
			)
	race_choices = (
				("Hispanic or Latino","Hispanic or Latino"),
				("Not Hispanic or Latino",
					"Not Hispanic or Latino"),
				("Asian","Asian"),
				("Black or African American",
					"Black or African American"),
				("White","White"),
				("American Indian/Alaska Native","American Indian/Alaska Native"),
				("Native Hawaiian or other Pacific Islander",
					"Native Hawaiian or other Pacific Islander"),
				("More than one race","More than one race"),
				("Unknown","Unknown"),
				("AA/Nat Am","AA/Nat Am"),
			)
	year_of_birth = forms.IntegerField()
	sero_positive_since = forms.IntegerField()
	gender = forms.CharField(widget=forms.Select(choices=gender_choices))
	race = forms.CharField(widget=forms.Select(choices=race_choices))

class PatientSelectOrAddForm(PatientForm):
	patient = forms.CharField(widget=forms.Select(choices= [[a.id,a.patient_id] for a in Patient.objects.all()]))
	def __init__(self,*args,**kwargs):
		super(PatientForm,self).__init__(*args,**kwargs)


class CaseReportFormWizard(FormWizard):
	def done(self,request,form_list):
		pass

	def alcohol_form(self):
		pass

	def drug_form(self):
		pass

	def hiv_form(self):
		pass

	def patient_form(self):
		pass

	def tobacco_form(self):
		pass

	def exposure_form(self):
		pass



class VisitForm(ModelForm):
	def __init__(self,postdata=None,visit_id=None,*args,**kwargs):
		super(ModelForm,self).__init__(*args, **kwargs)
		self.postdata = postdata
		if visit_id:
			self.visit_id = visit_id
		else:
			self.visit_id = None
	class Meta:
		model = Visit
	def save(self):
		v = Visit()
		if self.visit_id:
			v.id = self.visit_id
		v.patient = Patient.objects.get(pk=self.postdata['patient'])
		v.name = self.postdata['name']
		v.cd4 = self.postdata['cd4']
		v.dsg = self.postdata['dsg']
		v.viral = self.postdata['viral']

		# TODO: parse postdata['date'] into DateTime object

		# Insert into the database so we have a primary key
		v.save()

		# OK - now that we have a primary key we can insert the related
		# data

		for ill in self.postdata.getlist('illnesses'):
			i = PatientAdditionalIllnesses()
			i.visit = v
			i.illness = Illness.objects.get(pk=ill)
			i.save()

		for drug in self.postdata.getlist("drugs"):
			d = DrugUsed()
			d.visit = v
			d.drug = Drug.objects.get(pk=drug)
			d.save()

		for exp in self.postdata.getlist("exposures"):
			e = PatientExposedTo()
			e.visit = v
			e.exposure = Exposure.objects.get(pk=exp)
			e.save()