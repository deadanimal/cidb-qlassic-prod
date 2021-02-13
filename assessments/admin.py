from django.contrib import admin
from .models import QlassicAssessmentApplication, SupportingDocuments, SuggestedAssessor, AssignedAssessor, AssessmentData
# Register your models here.

class QAAAdmin(admin.ModelAdmin):
    list_display = ('qaa_number', 'user', 'application_status', 'created_date','modified_date',)

class SDAdmin(admin.ModelAdmin):
    list_display = ('qaa', 'file_name', 'created_date','modified_date',)

admin.site.register(QlassicAssessmentApplication, QAAAdmin)
admin.site.register(SupportingDocuments, SDAdmin)
admin.site.register(SuggestedAssessor)
admin.site.register(AssignedAssessor)
admin.site.register(AssessmentData)