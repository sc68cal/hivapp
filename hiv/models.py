# $Id$
from django.db import models
import reversion


class Drug(models.Model):
	"""
	Drug class encapsulates all the drugs that the study has encountered.
	Patients normally undergo a drug test, or a voluntary disclosure where
	they state what drugs they have used.
	"""
	class Meta:
		db_table = u'drug'
	def __unicode__(self):
		return self.name
	#id = models.IntegerField(primary_key=True)
	name = models.CharField(max_length=135, blank=True)


class Exposure(models.Model):
	"""List of things that a Patient could be exposed to."""

	class Meta:
		db_table = u'exposure'
	#id = models.IntegerField(primary_key=True)
	name = models.CharField(max_length=135, blank=True)

	def __unicode__(self):
		return self.name

class Illness(models.Model):
	"""
	Illness class encapsulates all the illnesses that the study tracks
	"""

	class Meta:
		db_table = u'illness'
		verbose_name_plural="Illnesses"
	#id = models.IntegerField(primary_key=True)
	name = models.CharField(max_length=135, blank=True)
	def __unicode__(self):
		return self.name


class Patient(models.Model):
	"""
	Class that encapsulates patients in the database

	This class represents a patient record, with fields representing
	clinical data. A patient can have 0 or many Visits
	"""
	class Meta:
		db_table = u'patient'
		ordering = ['patient_id']
	#id = models.IntegerField(primary_key=True)
	patient_id = models.CharField(max_length=135, blank=True)
	gender = models.CharField(max_length=135, blank=True)
	year_of_birth = models.IntegerField()
	sero_positive_since = models.IntegerField()
	lowest_cd4 = models.IntegerField(null=True, blank=True)
	highest_viral = models.IntegerField(null=True, blank=True)
	lowest_cd4_date = models.DateField(null=True, blank=True)
	highest_viral_date = models.DateField(null=True, blank=True)
	race = models.CharField(max_length=135, blank=True)

	def __unicode__(self):
		return self.patient_id

	@models.permalink
	def get_absolute_url(self):
    		return ('hiv.views.patient_detail', [str(self.id)])

class Visit(models.Model):
	"""
Visit represents all the actual clinical data, which is recorded each
time that a Patient comes in.

	"""
	class Meta:
		db_table = u'visit'
		ordering = ['name']
		verbose_name = "Patient Visit"
	#id = models.IntegerField(primary_key=True)
	patient = models.ForeignKey(Patient)
	date = models.DateField(null=True, blank=True)
	cd4 = models.CharField(max_length=135, blank=True)
	viral = models.CharField(max_length=135, blank=True)
	name = models.CharField(max_length=135, blank=True)
	dsg = models.IntegerField(null=True, blank=True)
	drugs = models.ManyToManyField(Drug, through="DrugUsed")
	exposures = models.ManyToManyField(Exposure, through="PatientExposedTo")
	illnesses = models.ManyToManyField(Illness,
						through=
						"PatientAdditionalIllnesses")

	def __unicode__(self):
		return self.name

	@models.permalink
	def get_absolute_url(self):
    		return ('helix.hiv.views.visit_detail', [str(self.id)])



class DrugTest(models.Model):
	'''
	DrugTest: Currently not implemented. The original clinical data did not
	have very good record keeping about what drugs were tested / when tested / etc.

	A design decision was made to just use the rows in the original data where drugs
	that a patent had either admitted to, or tested positive for
	were checked off.

	'''
	class Meta:
		db_table = u'drug_test'
	#id = models.IntegerField(primary_key=True)
	drug = models.ForeignKey(Drug)
	visit = models.ForeignKey(Visit)
	result = models.IntegerField(null=True, blank=True)



class DrugUsed(models.Model):
	'''
	DrugUsed: Encapsulates the ManyToMany relationship between a Patient,
	and the drug(s) that they have either tested positive for, or admitted during
	a Visit.

	'''
	class Meta:
		db_table = u'drug_used'
		verbose_name = "Patient Drug History"
		verbose_name_plural = "Patient Drug Histories"
	#id = models.IntegerField(primary_key=True)
	visit = models.ForeignKey(Visit)
	drug = models.ForeignKey(Drug)
	frequency = models.IntegerField(null=True, blank=True)
	date_stopped = models.DateField()
	use_before_infected = models.IntegerField(null=True, blank=True)
	use_after_infected = models.IntegerField(null=True, blank=True)

	
	def __unicode__(self):
		return self.visit.name + "-" + self.drug.name


class HivdTest(models.Model):
	'''
	Class HivdTest: Not implemented. Some data from the original spreasheet
	mentioned HIV tests that a patient might have had done during a Visit
	'''
	class Meta:
		db_table = u'hivd_test'
		verbose_name = "HIV Test"
	#id = models.IntegerField(primary_key=True)
	score = models.CharField(max_length=135, blank=True)
	type = models.CharField(max_length=135, blank=True)
	visit = models.ForeignKey(Visit)



class Mutation(models.Model):
	'''
	Class Mutation: Encapsulates the SNP data that is taken each time a Patient
	has a Visit.

	'''
	class Meta:
		db_table = u'mutation'
	#id = models.IntegerField(primary_key=True)
	visit = models.ForeignKey(Visit)
	read_start = models.IntegerField(null=True, blank=True)
	read_end = models.IntegerField(null=True, blank=True)

	def __unicode__(self):
		return self.visit.name + " " \
			+ str(self.read_start) + "-" + str(self.read_end)

	def get_length(self):
		return self.read_end - self.read_start

	@models.permalink
	def get_absolute_url(self):
    		return ('helix.hiv.views.mutation_detail', [str(self.id)])


class MutationFile(models.Model):
	'''
	Class MutationFile: Not Implemented. Should store the original SNP files as
	a binary blob.
	'''
	class Meta:
		db_table = u'mutation_file'
	#id = models.IntegerField(primary_key=True)
	mutation = models.ForeignKey(Mutation)
	file = models.TextField(blank=True)


class MutationPosition(models.Model):
	'''
	Class MutationPostion: Within a SNP data sample, if there is a mutation at
	a position, this is where the actual mutation data is stored. Encapsulates the
	1->M relationship between a SNP data sample and the mutations that it has.
	'''
	class Meta:
		db_table = u'mutation_position'
	#id = models.IntegerField(primary_key=True)
	mutation = models.ForeignKey(Mutation)
	position = models.IntegerField(null=True, blank=True)
	ref_nt = models.CharField(max_length=3, blank=True)
	mut_nt = models.CharField(max_length=3, blank=True)

	
	def __unicode__(self):
		return self.mutation.__unicode__() + " at " + str(self.position)





class PatientAdditionalIllnesses(models.Model):
	'''
	Class PatientAdditionalIllnesses: Encapsulates the 1->M relationship between the
	illnesses that a Patient can be suffering from when they have a Visit.
	'''
	class Meta:
		db_table = u'patient_additional_illnesses'
		verbose_name = "Patient Illness"
		verbose_name_plural= "Patient Illnesses"
	#id = models.IntegerField(primary_key=True)
	illness = models.ForeignKey(Illness)
	visit = models.ForeignKey(Visit)

	def __unicode__(self):
		return self.visit.name + "-" + self.illness.name


class PatientExposedTo(models.Model):
	'''
	Class PatientExposedTo:	Encapsulates the 1->M relationship between the exposures
	that a Patient can disclose in the course of a Visit.
	'''
	class Meta:
		db_table = u'patient_exposed_to'
		verbose_name="Patient Exposure"
	#id = models.IntegerField(primary_key=True)
	visit = models.ForeignKey(Visit)
	exposure = models.ForeignKey(Exposure)

	def __unicode__(self):
		return self.visit.name + "-" + self.exposure.name



class Sequence(models.Model):
	'''
	Class Sequence: Not Implemented.
	'''
	class Meta:
		db_table = u'sequence'

	#id = models.IntegerField(primary_key=True)
	c_ebp_ii = models.CharField(max_length=135,
			db_column='C_EBP_II',
			blank=True) # Field name made lowercase.

	usf = models.CharField(max_length=135,
			db_column='USF',
			blank=True) # Field name made lowercase.

	ets = models.CharField(max_length=135,
				db_column='Ets',
				blank=True) # Field name made lowercase.

	lef_1 = models.CharField(max_length=135,
					db_column='Lef_1',
					blank=True) # Field name made lowercase.

	atf_creb = models.CharField(max_length=135,
					db_column='ATF_CREB',
					blank=True) # Field name made lowercase.
	lef_1_atf_creb_insertions = models.CharField(max_length=135)
	c_ebp_i = models.CharField(max_length=135,
				db_column='C_EBP_I',
				blank=True) # Field name made lowercase.
	nfkb_ii = models.CharField(max_length=135,
				db_column='NFKB_II',
				blank=True) # Field name made lowercase.

	nfkb_i = models.CharField(max_length=135,
				db_column='NFKB_I',
				blank=True) # Field name made lowercase.

	sp_iii = models.CharField(max_length=135,
				db_column='SP_III',
				blank=True) # Field name made lowercase.
	sp_ii = models.CharField(max_length=135,
				db_column='SP_II',
				blank=True) # Field name made lowercase.

	sp_i = models.CharField(max_length=135, 
				db_column='SP_I',
				blank=True) # Field name made lowercase.

	oct_i = models.CharField(max_length=135,
				db_column='OCT_I',
				blank=True) # Field name made lowercase.
	visit = models.ForeignKey(Visit)
