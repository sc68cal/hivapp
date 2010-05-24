# $Id$
from hiv.models import *
from django.contrib import admin

admin.site.register(Patient)
admin.site.register(Drug)
admin.site.register(Visit)
admin.site.register(DrugTest)
admin.site.register(DrugUsed)
admin.site.register(Exposure)
admin.site.register(Illness)
admin.site.register(Mutation)
admin.site.register(MutationFile)
admin.site.register(MutationPosition)
admin.site.register(PatientAdditionalIllnesses)
admin.site.register(PatientExposedTo)
admin.site.register(Sequence)
