from django.forms import ModelForm
from django import forms

from .models import DefectGroup, SubComponent, Element, Component, QlassicAssessmentApplication, SupportingDocuments


from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column, Field

class ComponentCreateForm(ModelForm):
    class Meta:
        model = Component
        fields = (
            'name',
            'type',
            'weightage',
        )

class SubComponentCreateForm(ModelForm):
    class Meta:
        model = SubComponent
        fields = (
            'name',
            'type',
            # 'no_of_check',
            # 'weightage',
        )

class ElementCreateForm(ModelForm):
    class Meta:
        model = Element
        fields = (
            'name',
            'no_of_check',
            # 'sub_component_weightage',
            'weightage',
        )

class DefectGroupCreateForm(ModelForm):

    class Meta:
        model = DefectGroup
        fields = (
            'name',
        )

class ComponentEditForm(ModelForm):
    class Meta:
        model = Component
        fields = (
            'name',
            'type',
            'weightage',
        )

class SubComponentEditForm(ModelForm):
    class Meta:
        model = SubComponent
        fields = (
            'name',
            'type',
            # 'no_of_check',
            # 'weightage',
        )

class ElementEditForm(ModelForm):
    class Meta:
        model = Element
        fields = (
            'name',
            'no_of_check',
            'weightage',
        )

# class ElementWithWeightageEditForm(ModelForm):
#     class Meta:
#         model = Element
#         fields = (
#             'name',
#             'no_of_check',
#             'weightage',
#         )

class DefectGroupEditForm(ModelForm):

    class Meta:
        model = DefectGroup
        fields = (
            'name',
        )


# class SupportingDocumentsUploadForm(ModelForm):
#     file = forms.FileField(
#         label='',
#         widget=forms.FileInput(
#             attrs={
#                 'class': 'form-control'
#                 } 
#         )
#     )
#     class Meta:
#         model = SupportingDocuments
#         fields = ('file',)

class SupportingDocumentsUploadForm(forms.Form):
    sd_1 = forms.FileField(required=False)
    sd_2 = forms.FileField(required=False)
    sd_3 = forms.FileField(required=False)
    sd_4 = forms.FileField(required=False)
    sd_5 = forms.FileField(required=False)
    sd_6 = forms.FileField(required=False)
    sd_7 = forms.FileField(required=False)
    sd_8 = forms.FileField(required=False)
    sd_9 = forms.FileField(required=False)

class QAACreateForm(ModelForm):
    class Meta:
        model = QlassicAssessmentApplication
        readonly = ('role',)
        fields = (
            'applicant_name',
            'role',
            'organization',
            'address1',
            'address2',
            'city',
            'state',
            'postcode',
            'email',
            'hp_no',
            'fax_no',
            'contract_type',
            'building_type',
            'proposed_date',
        )

class QAAApplicationForm(ModelForm):
    class Meta:
        model = QlassicAssessmentApplication
        fields = ('building_type','proposed_date','contract_type')

class QAAReviewForm(ModelForm):
    class Meta:
        model = QlassicAssessmentApplication
        fields = (
            'proposed_date',
            'no_of_assessor',
            'no_of_blocks',
            'no_of_days',
            'payment_mode',
            'remarks1',
        )

class QAAVerifyForm(ModelForm):
    class Meta:
        model = QlassicAssessmentApplication
        fields = (
            'assessment_date',
            'no_of_assessor',
            'no_of_blocks',
            'no_of_days',
            'payment_mode',
            'remarks2',
        )