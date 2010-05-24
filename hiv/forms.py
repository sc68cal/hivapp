from django.forms import ModelForm
from django import forms
from helix.hiv.models import *



class VisitForm(ModelForm):
	class Meta:
		model = Visit
		fields = ('patient','date','viral','name','dsg','drugs',
			'exposures','illnesses',
			)
		
class PatientSearchForm(ModelForm):
	class Meta:
		model = Patient
		fields = ('name',)


# TODO: Create race table and do a ManyToMany foreign key
class PatientForm(ModelForm):
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
			)
	year_of_birth = forms.IntegerField()
	sero_positive_since = forms.IntegerField()
	gender = forms.CharField(widget=forms.Select(choices=gender_choices))
	race = forms.CharField(widget=forms.Select(choices=race_choices))
	class Meta:
		model = Patient
		fields = ('name','gender','year_of_birth','sero_positive_since',
			'lowest_cd4','highest_viral','highest_viral_date',
			'race',)