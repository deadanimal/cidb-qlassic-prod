from django.contrib import admin
from .models import Contractor, VerifiedContractor, ProjectInfo

class PIAdmin(admin.ModelAdmin):
    list_display = ('project_title', 'project_reference_number', 'created_date','modified_date',)

class ContractorAdmin(admin.ModelAdmin):
    list_display = ('project_title', 'project_reference_number', 'applied', 'created_date','modified_date',)

# Register your models here.
admin.site.register(Contractor, ContractorAdmin)
admin.site.register(VerifiedContractor)
admin.site.register(ProjectInfo, PIAdmin)