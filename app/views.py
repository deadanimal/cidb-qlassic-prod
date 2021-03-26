# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.http.response import JsonResponse
from assessments.views import get_qaa_result
from datetime import date, datetime
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.template import loader
from django.http import HttpResponse, Http404
from django import template
from django.contrib import messages
from django.urls import resolve
from django.db.models import Q

# XHTML2PDF
from app.xhtml2pdf import link_callback
from xhtml2pdf import pisa 
from django.template.loader import get_template

# Helpers
from app.helpers.letter_templates import test_letter_template
from portal.helpers import TEMPLATE_TYPE
from trainings.helpers import get_pass_fail_translation

# Forms
from assessments.forms import DefectGroupCreateForm, SubComponentCreateForm, ElementCreateForm, ComponentCreateForm
from projects.forms import VerifiedContractorForm
from portal.forms import LetterTemplateCreateForm, LetterTemplateTrainingCreateForm
from trainings.forms import TrainingTypeCreateForm

# Models
from assessments.models import DefectGroup, SubComponent, Element, Component, QlassicAssessmentApplication, SupportingDocuments
from trainings.models import TrainingType, Training
from projects.models import ProjectInfo, VerifiedContractor
from portal.models import Announcement, Publication, LetterTemplate

# Generate Document
from core.helpers import translate_malay_date, standard_date
from app.helpers.letter_templates import generate_document, generate_document_file

# Decorators
from authentication.decorators import allowed_users

# SOAP
from api.soap.get_contractor import verify_contractor

### Landing Page ###
# @login_required(login_url="/login/")
def index(request):
    announcements = Announcement.objects.all()
    publications = Publication.objects.all()
    context = {'announcements':announcements,'publications':publications}
    return render(request, "index.html", context)

def assessment(request):
    return render(request, "assessment.html")

def training(request):
    trainings = Training.objects.all().filter(review_status='accepted',publish=True)
    context = {'trainings':trainings}
    return render(request, "training.html", context)

def contact(request):
    return render(request, "contact.html")

def announcement(request, id):
    content = get_object_or_404(Announcement, id=id)
    mode = 'announcement'
    context = {
        'content':content,
        'mode':mode,
    }
    return render(request, "detail.html", context)

def publication(request, id):
    content = get_object_or_404(Publication, id=id)
    mode = 'publication'
    context = {
        'content':content,
        'mode':mode,
    }
    return render(request, "detail.html", context)

### Admin - Reporting & Certification Module ###
@login_required(login_url="/login/")
def dashboard_report_list(request):
    projects = QlassicAssessmentApplication.objects.all().filter(
        Q(application_status='completed')|
        Q(application_status='approved')
    )
    context = {
        'projects':projects,
    }
    return render(request, "dashboard/reporting/report_list.html", context)

@login_required(login_url="/login/")
def dashboard_qlassic_report_view(request, report_type, id):
    qaa = get_object_or_404(QlassicAssessmentApplication, id=id)
    mode = 'view'
    context = {
        'qaa':qaa,
        'report_type':report_type,
        'mode':mode,
    }
    return render(request, "dashboard/reporting/report_detail.html", context)

@login_required(login_url="/login/")
def dashboard_report_review(request, report_type, id):
    qaa = get_object_or_404(QlassicAssessmentApplication, id=id)
    mode = 'review'
    context = {
        'qaa':qaa,
        'report_type':report_type,
        'mode':mode,
    }
    return render(request, "dashboard/reporting/report_detail.html", context)

@login_required(login_url="/login/")
def dashboard_report_verify(request, report_type, id):
    qaa = get_object_or_404(QlassicAssessmentApplication, id=id)
    mode = 'verify'
    context = {
        'qaa':qaa,
        'report_type':report_type,
        'mode':mode,
    }
    return render(request, "dashboard/reporting/report_detail.html", context)

@login_required(login_url="/login/")
def dashboard_report_approve(request, report_type, id):
    qaa = get_object_or_404(QlassicAssessmentApplication, id=id)
    mode = 'approve'
    context = {
        'qaa':qaa,
        'report_type':report_type,
        'mode':mode,
    }
    return render(request, "dashboard/reporting/report_detail.html", context)

# def report_view(request, report_type, id):
#     qaa = get_object_or_404(QlassicAssessmentApplication, id=id)
#     template_path = ''
#     if report_type == 'score_letter':
#         template_path = 'pdf/score_letter.html'
#     elif report_type == 'qlassic_report':
#         template_path = 'pdf/qlassic_report.html'
#     elif report_type == 'qlassic_certificate':
#         template_path = 'pdf/qlassic_certificate.html'
#     else:
#         raise Http404
#     qr_url = request.build_absolute_uri()
#     host_url = request.scheme+'://'+request.META['HTTP_HOST'] 
#     context = {
#         'host_url': host_url,
#         'qr_url': qr_url,
#         'qaa': qaa
#     }
#     return render(request, template_path, context)

# def report_generate(request, report_type, id):
#     template_path = ''
#     if report_type == 'score_letter':
#         template_path = 'pdf/score_letter.html'
#     elif report_type == 'qlassic_report':
#         template_path = 'pdf/qlassic_report.html'
#     elif report_type == 'qlassic_certificate':
#         template_path = 'pdf/qlassic_certificate.html'
#     else:
#         raise Http404

#     qaa = get_object_or_404(QlassicAssessmentApplication, id=id)
#     qr_url = request.build_absolute_uri()
#     host_url = request.scheme+'://'+request.META['HTTP_HOST'] 
#     context = {
#         'host_url': host_url,
#         'qr_url': qr_url,
#         'qaa': qaa
#     }
#     # Create a Django response object, and specify content_type as pdf
#     response = HttpResponse(content_type='application/pdf')
#     # response['Content-Disposition'] = 'attachment; filename="report.pdf"'
#     response['Content-Disposition'] = 'inline; filename="report.pdf"'
#     # find the template and render it.
#     template = get_template(template_path)
#     html = template.render(context)

#     # create a pdf
#     pisa_status = pisa.CreatePDF(
#        html, dest=response, link_callback=link_callback)
#     # if error then show some funy view
#     if pisa_status.err:
#        return HttpResponse('We had some errors <pre>' + html + '</pre>')
#     return response

def qlassic_report_generate(request, report_type, id):
    qaa = get_object_or_404(QlassicAssessmentApplication, id=id)
    tmpl_ctx = ''
    if report_type == 'qlassic_score_letter':
        tmpl_ctx = {
            'title': qaa.pi.project_title,
            'qaa_number': qaa.qaa_number,
            'assessment_date': translate_malay_date(standard_date(qaa.assessment_date)),
            'developer': qaa.pi.developer,
            'developer_ssm_number': qaa.pi.developer_ssm_number,
            'contractor': qaa.pi.contractor_name,
            'cidb_number': qaa.pi.contractor_cidb_registration_no,
            'grade': qaa.pi.contractor_registration_grade,
            'ccd_score': '',
            'qlassic_score': '',
        }
    elif report_type == 'qlassic_report':
        tmpl_ctx = {
            'title': qaa.pi.project_title,
            'qaa_number': qaa.qaa_number,
            'assessment_date': translate_malay_date(standard_date(qaa.assessment_date)),
            'developer': qaa.pi.developer,
            'developer_ssm_number': qaa.pi.developer_ssm_number,
            'contractor': qaa.pi.contractor_name,
            'cidb_number': qaa.pi.contractor_cidb_registration_no,
            'grade': qaa.pi.contractor_registration_grade,
            'ccd_score': '',
            'qlassic_score': '',
        }
    elif report_type == 'qlassic_certificate':
        tmpl_ctx = {
            'title': qaa.pi.project_title,
            'qaa_number': qaa.qaa_number,
            'assessment_date': translate_malay_date(standard_date(qaa.assessment_date)),
            'developer': qaa.pi.developer,
            'developer_ssm_number': qaa.pi.developer_ssm_number,
            'contractor': qaa.pi.contractor_name,
            'cidb_number': qaa.pi.contractor_cidb_registration_no,
            'grade': qaa.pi.contractor_registration_grade,
            'ccd_score': '',
            'qlassic_score': '',
        }
    else:
        raise Http404
    qr_url = request.build_absolute_uri()
    host_url = request.scheme+'://'+request.META['HTTP_HOST'] 
    context = {
        'host_url': host_url,
        'qr_url': qr_url,
        'qaa': qaa
    }
    response = generate_document(request, report_type, tmpl_ctx)
    
    return response

def report_generate(request, report_type, id):
    template_path = ''
    if report_type == 'score_letter':
        template_path = 'pdf/score_letter.html'
    elif report_type == 'qlassic_report':
        template_path = 'pdf/qlassic_report.html'
    elif report_type == 'qlassic_certificate':
        template_path = 'pdf/qlassic_certificate.html'
    else:
        raise Http404

    qaa = get_object_or_404(QlassicAssessmentApplication, id=id)
    qr_url = request.build_absolute_uri()
    host_url = request.scheme+'://'+request.META['HTTP_HOST'] 
    context = {
        'host_url': host_url,
        'qr_url': qr_url,
        'qaa': qaa
    }
    # Create a Django response object, and specify content_type as pdf
    response = HttpResponse(content_type='application/pdf')
    # response['Content-Disposition'] = 'attachment; filename="report.pdf"'
    response['Content-Disposition'] = 'inline; filename="report.pdf"'
    # find the template and render it.
    template = get_template(template_path)
    html = template.render(context)

    # create a pdf
    pisa_status = pisa.CreatePDF(
       html, dest=response, link_callback=link_callback)
    # if error then show some funy view
    if pisa_status.err:
       return HttpResponse('We had some errors <pre>' + html + '</pre>')
    return response

from .helpers.letter_templates import generate_training_document

from core.helpers import send_email_with_attachment
from trainings.models import RegistrationTraining
from api.soap.create_transaction import get_kodhasil, cancel_proforma

@login_required(login_url="/login/")
def view_pdf(request):
    qaa = QlassicAssessmentApplication.objects.all().filter(application_status="assessor_assign").first()
    result = get_qaa_result(qaa)
    # get_kodhasil("QLC")
    # response = generate_document_file(request, 'training_certificate', {})
    # response = get_kodhasil('YKSHEQ')
    # # print(response)
    # # response = get_kodhasil('QLC')
    # training_type = TrainingType.objects.all().filter(name="Exam")[0]
    # template_ctx = {
    #     'name': 'Abu bin Ali',
    #     'hp_no': '011-110220',
    #     'fax_no': '011-110220',
    #     'address1': 'Lolololo',
    #     'address2': 'Lilililili',
    #     'postcode': '192200',
    #     'city': 'Kota Bharu',
    #     'state': 'Kelantan',
    #     'company': 'Kelantan Sdn. Bhd.',
    #     'date': translate_malay_date(standard_date(datetime.now().date())),
    #     'current_date': translate_malay_date(standard_date(datetime.now().date())),
    #     'location': 'Seri Kamanban',
    #     'ic': '920202-1020-1200',
    #     'pass': get_pass_fail_translation(True),
    # }
    # # cancel_proforma("PFHQB42103000027")
    # response = generate_training_document(request, training_type, template_ctx)
    # # SupportingDocuments.objects.create(file_name=response['name'],file=response['path'])
    
    # attendance = RegistrationTraining.objects.all().exclude(certificate_file=None).first()

    # haha = '{0:03d}'.format(int(2000)+1)
    # print(haha)
    # Email
    # to = ['muhaafidz@gmail.com']
    # subject = "Complaint From Trainee"
    # attachments = [attendance.certificate_file.path]
    # messages.info(request, 'Successfully delivered an email to trainer(s).')
    # send_email_with_attachment(subject, to, {}, 'email/training-complaint.html', attachments)
    return JsonResponse(result,safe=False, json_dumps_params={'indent': 4})

@login_required(login_url="/login/")
def generate_pdf(request):
    template_path = 'pdf/score_letter.html'
    qaa = QlassicAssessmentApplication.objects.all()[:0]
    context = {
        'qaa': qaa
    }
    # Create a Django response object, and specify content_type as pdf
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="report.pdf"'
    # find the template and render it.
    template = get_template(template_path)
    html = template.render(context)

    # create a pdf
    pisa_status = pisa.CreatePDF(
       html, dest=response, link_callback=link_callback)
    # if error then show some funy view
    if pisa_status.err:
       return HttpResponse('We had some errors <pre>' + html + '</pre>')
    return response

### Admin - Management Module ###
@login_required(login_url="/login/")
@allowed_users(allowed_roles=['superadmin'])
def dashboard_defect_group(request):
    defect_groups = DefectGroup.objects.all()
    form_defect_group = DefectGroupCreateForm()
    if request.method == 'POST':
        if 'create' in request.POST:
            form_defect_group = DefectGroupCreateForm(request.POST)
            if form_defect_group.is_valid():
                form_defect_group.save()
                messages.info(request, 'Created successfully')
            else:
                messages.warning(request, 'Unable to create new defect group')

        return redirect('dashboard_defect_group')
    context = {"defect_groups": defect_groups, 'form_defect_group': form_defect_group}
    return render(request, "dashboard/management/defect_group.html", context)

@login_required(login_url="/login/")
@allowed_users(allowed_roles=['superadmin'])
def dashboard_defect_group_id(request, id):
    defect_group = get_object_or_404(DefectGroup, id=id)
    form_defect_group = DefectGroupCreateForm(instance=defect_group)
    if request.method == 'POST':
        if 'delete' in request.POST:
            defect_group.delete()
            messages.info(request, 'Deleted successfully')
            return redirect('dashboard_defect_group')
        if 'update' in request.POST:
            form_defect_group = DefectGroupCreateForm(request.POST,instance=defect_group)
            if form_defect_group.is_valid():
                form_defect_group.save()
                messages.info(request, 'Updated successfully')
            else:
                messages.warning(request, 'Unable to update defect_group')

        return redirect('dashboard_defect_group_id', id)
    context = {"defect_group": defect_group,'form_defect_group':form_defect_group}
    return render(request, "dashboard/management/defect_group_id.html", context)

@login_required(login_url="/login/")
@allowed_users(allowed_roles=['superadmin'])
def dashboard_sub_component(request):
    sub_components = SubComponent.objects.all()
    form_sub_component = SubComponentCreateForm()
    if request.method == 'POST':
        if 'create' in request.POST:
            form_sub_component = SubComponentCreateForm(request.POST)
            if form_sub_component.is_valid():
                form_sub_component.save()
                messages.info(request, 'Created successfully')
            else:
                messages.warning(request, 'Unable to create new sub_component')

        return redirect('dashboard_sub_component')
    context = {"sub_components": sub_components, 'form_sub_component': form_sub_component}
    return render(request, "dashboard/management/sub_component.html", context)

@login_required(login_url="/login/")
@allowed_users(allowed_roles=['superadmin'])
def dashboard_sub_component_id(request, id):
    sub_component = get_object_or_404(SubComponent, id=id)
    form_sub_component = SubComponentCreateForm(instance=sub_component)
    if request.method == 'POST':
        if 'delete' in request.POST:
            sub_component.delete()
            messages.info(request, 'Deleted successfully')
            return redirect('dashboard_sub_component')
        if 'update' in request.POST:
            form_sub_component = SubComponentCreateForm(request.POST,instance=sub_component)
            if form_sub_component.is_valid():
                form_sub_component.save()
                messages.info(request, 'Updated successfully')
            else:
                messages.warning(request, 'Unable to update sub_component')

        return redirect('dashboard_sub_component_id', id)
    context = {"sub_component": sub_component,'form_sub_component':form_sub_component}
    return render(request, "dashboard/management/sub_component_id.html", context)

@login_required(login_url="/login/")
@allowed_users(allowed_roles=['superadmin'])
def dashboard_component(request):
    components = Component.objects.all()
    form_component = ComponentCreateForm()
    if request.method == 'POST':
        if 'create' in request.POST:
            form_component = ComponentCreateForm(request.POST)
            if form_component.is_valid():
                form_component.save()
                messages.info(request, 'Created successfully')
            else:
                messages.warning(request, 'Unable to create new component')

        return redirect('dashboard_component')
    context = {"components": components, 'form_component': form_component}
    return render(request, "dashboard/management/component.html", context)

@login_required(login_url="/login/")
@allowed_users(allowed_roles=['superadmin'])
def dashboard_component_id(request, id):
    component = get_object_or_404(Component, id=id)
    form_component = ComponentCreateForm(instance=component)
    if request.method == 'POST':
        if 'delete' in request.POST:
            component.delete()
            messages.info(request, 'Deleted successfully')
            return redirect('dashboard_component')
        if 'update' in request.POST:
            form_component = ComponentCreateForm(request.POST,instance=component)
            if form_component.is_valid():
                form_component.save()
                messages.info(request, 'Updated successfully')
            else:
                messages.warning(request, 'Unable to update component')

        return redirect('dashboard_component_id', id)
    context = {"component": component,'form_component':form_component}
    return render(request, "dashboard/management/component_id.html", context)

@login_required(login_url="/login/")
@allowed_users(allowed_roles=['superadmin'])
def dashboard_element(request):
    elements = Element.objects.all()
    form_element = ElementCreateForm()
    if request.method == 'POST':
        if 'create' in request.POST:
            form_element = ElementCreateForm(request.POST)
            if form_element.is_valid():
                form_element.save()
                messages.info(request, 'Created successfully')
            else:
                messages.warning(request, 'Unable to create new element.')

        return redirect('dashboard_element')
    context = {"elements": elements, 'form_element': form_element}
    return render(request, "dashboard/management/element.html", context)

@login_required(login_url="/login/")
@allowed_users(allowed_roles=['superadmin'])
def dashboard_element_id(request, id):
    element = get_object_or_404(Element, id=id)
    form_element = ElementCreateForm(instance=element)
    if request.method == 'POST':
        if 'delete' in request.POST:
            element.delete()
            messages.info(request, 'Deleted successfully')
            return redirect('dashboard_element')
        if 'update' in request.POST:
            form_element = ElementCreateForm(request.POST,instance=element)
            if form_element.is_valid():
                form_element.save()
                messages.info(request, 'Updated successfully')
            else:
                messages.warning(request, 'Unable to update element.')

        return redirect('dashboard_element_id', id)
    context = {"element": element,'form_element':form_element}
    return render(request, "dashboard/management/element_id.html", context)

@login_required(login_url="/login/")
@allowed_users(allowed_roles=['superadmin'])
def dashboard_management_letter_id(request, id):
    context = {
    }
    return render(request, "dashboard/management/letter_id.html", context)

@login_required(login_url="/login/")
@allowed_users(allowed_roles=['superadmin'])
def dashboard_management_letter(request):
    context = {
    }
    return render(request, "dashboard/management/letter.html", context)

@login_required(login_url="/login/")
@allowed_users(allowed_roles=['superadmin'])
def dashboard_verified_contractor(request):
    vcs = VerifiedContractor.objects.all()
    form_vc = VerifiedContractorForm()
    if request.method == 'POST':
        if 'create' in request.POST:
            form_vc = VerifiedContractorForm(request.POST)
            contractor_registration_number = request.POST['contractor_registration_number']
            found = verify_contractor(contractor_registration_number)
            if found is True:
                if form_vc.is_valid():
                    vc = form_vc.save()
                    messages.info(request, 'Created successfully')
                else:
                    messages.warning(request, 'Unable to create new verified contractor:'+form_vc.errors.as_text())
            else:
                messages.warning(request, 'Unable to create new verified contractor: Record not found in CIMS System.')

        return redirect('dashboard_verified_contractor')
    context = {"vcs": vcs, 'form_vc': form_vc}
    return render(request, "dashboard/management/verified_contractor.html", context)

@login_required(login_url="/login/")
@allowed_users(allowed_roles=['superadmin'])
def dashboard_verified_contractor_id(request, id):
    vc = get_object_or_404(VerifiedContractor, id=id)
    form_vc = VerifiedContractorForm(instance=vc)
    if request.method == 'POST':
        if 'delete' in request.POST:
            vc.delete()
            messages.info(request, 'Deleted successfully')
            return redirect('dashboard_verified_contractor')
        if 'update' in request.POST:
            form_vc = VerifiedContractorForm(request.POST,instance=vc)
            contractor_registration_number = request.POST['contractor_registration_number']
            found = verify_contractor(contractor_registration_number)
            if found is True:
                if form_vc.is_valid():
                    form_vc.save()
                    messages.info(request, 'Updated successfully')
                else:
                    messages.warning(request, 'Unable to update verified contractor:'+form_vc.errors.as_text())
            else:
                messages.warning(request, 'Unable to update new verified contractor: Record not found in CIMS System.')

        return redirect('dashboard_verified_contractor_id', id)
    context = {"vc": vc,'form_vc':form_vc}
    return render(request, "dashboard/management/verified_contractor_id.html", context)

@login_required(login_url="/login/")
@allowed_users(allowed_roles=['superadmin'])
def dashboard_letter_template(request):
    letter_templates = LetterTemplate.objects.all().filter(training_type=None)
    form_letter_template = LetterTemplateCreateForm()
    
    # Check Template Existence
    for tt in TEMPLATE_TYPE:
        lt = LetterTemplate.objects.all().filter(template_type=tt[0],is_active=True)
        if len(lt) > 0:
            pass
        else:
            messages.warning(request, "Template '" + tt[1] + "' does not exist or inactive. Please upload the following template.")

    if request.method == 'POST':
        if 'create' in request.POST:
            form_letter_template = LetterTemplateCreateForm(request.POST,request.FILES)
            if form_letter_template.is_valid():
                form_letter_template.save()
                messages.info(request, 'Created successfully')
            else:
                messages.warning(request, 'Unable to create new letter template: '+form_letter_template.errors.as_text())
        if 'test_template' in request.POST:
            id = request.POST['id']
            template_type = request.POST['template_type']
            response = test_letter_template(id, template_type)
            return response

        return redirect('dashboard_letter_template')
    context = {"letter_templates": letter_templates, 'form_letter_template': form_letter_template}
    return render(request, "dashboard/management/letter_template.html", context)

@login_required(login_url="/login/")
@allowed_users(allowed_roles=['superadmin'])
def dashboard_letter_template_id(request, id):
    letter_template = get_object_or_404(LetterTemplate, id=id)
    form_letter_template = LetterTemplateCreateForm(instance=letter_template)
    if request.method == 'POST':
        if 'delete' in request.POST:
            letter_template.delete()
            messages.info(request, 'Deleted successfully')
            return redirect('dashboard_letter_template')
        if 'update' in request.POST:
            form_letter_template = LetterTemplateCreateForm(request.POST,request.FILES,instance=letter_template)
            if form_letter_template.is_valid():
                form_letter_template.save()
                messages.info(request, 'Updated successfully')
            else:
                messages.warning(request, 'Unable to update letter_template')

        return redirect('dashboard_letter_template_id', id)
    context = {"letter_template": letter_template,'form_letter_template':form_letter_template}
    return render(request, "dashboard/management/letter_template_id.html", context)

@login_required(login_url="/login/")
@allowed_users(allowed_roles=['superadmin'])
def dashboard_training_type(request):
    training_types = TrainingType.objects.all()
    form_training_type = TrainingTypeCreateForm()
    form_letter_template = LetterTemplateTrainingCreateForm()
    if request.method == 'POST':
        if 'create' in request.POST:
            form_training_type = TrainingTypeCreateForm(request.POST,request.FILES)
            form_letter_template = LetterTemplateTrainingCreateForm(request.POST,request.FILES)
            if form_training_type.is_valid():
                if form_letter_template.is_valid():
                    training_type = form_training_type.save()
                    letter_template = form_letter_template.save()
                    letter_template.training_type = training_type
                    letter_template.title = training_type.name
                    letter_template.type = training_type.name
                    letter_template.save()
                    messages.info(request, 'Created successfully')
                else:
                    messages.warning(request, 'Unable to create new training type: '+form_training_type.errors.as_text())
            else:
                messages.warning(request, 'Unable to create new training type: '+form_training_type.errors.as_text())

        return redirect('dashboard_training_type')
    context = {"training_types": training_types, 'form_training_type': form_training_type, 'form_letter_template': form_letter_template}
    return render(request, "dashboard/management/training_type.html", context)

@login_required(login_url="/login/")
@allowed_users(allowed_roles=['superadmin'])
def dashboard_training_type_id(request, id):
    training_type = get_object_or_404(TrainingType, id=id)
    letter_template = get_object_or_404(LetterTemplate, training_type=training_type)
    form_training_type = TrainingTypeCreateForm(instance=training_type)
    form_letter_template = LetterTemplateTrainingCreateForm(instance=letter_template)
    if request.method == 'POST':
        if 'delete' in request.POST:
            letter_template.delete()
            training_type.delete()
            messages.info(request, 'Deleted successfully')
            return redirect('dashboard_training_type')
        if 'update' in request.POST:
            form_training_type = TrainingTypeCreateForm(request.POST,request.FILES,instance=training_type)
            form_letter_template = LetterTemplateTrainingCreateForm(request.POST,request.FILES,instance=letter_template)
            if form_training_type.is_valid():
                if form_letter_template.is_valid():
                    form_training_type.save()
                    form_letter_template.save()
                    messages.info(request, 'Updated successfully')
                else:
                    messages.warning(request, 'Unable to update training type')
            else:
                messages.warning(request, 'Unable to update training type')

        return redirect('dashboard_training_type_id', id)
    context = {"training_type": training_type,'form_training_type':form_training_type, 'form_letter_template':form_letter_template}
    return render(request, "dashboard/management/training_type_id.html", context)

# @login_required(login_url="/login/")
def pages(request):
    context = {}
    # All resource paths end in .html.
    # Pick out the html file name from the url. And load that template.
    try:
        
        load_template = request.path.split('/')[-1]
        html_template = loader.get_template( load_template )
        return HttpResponse(html_template.render(context, request))
        
    except template.TemplateDoesNotExist:

        html_template = loader.get_template( 'page-404.html' )
        return HttpResponse(html_template.render(context, request))

    except:
    
        html_template = loader.get_template( 'page-500.html' )
        return HttpResponse(html_template.render(context, request))

from django.db.models import Count, Sum

@login_required(login_url="/login/")
@allowed_users(allowed_roles=['superadmin'])
def dashboard_manage_component_v2(request):
    components = Component.objects.all()
    elements = Element.objects.all().filter(category_weightage=True)
    total_weightage_a = components.aggregate(Sum('weightage_a'))
    total_weightage_b = components.aggregate(Sum('weightage_b'))
    total_weightage_c = components.aggregate(Sum('weightage_c'))
    total_weightage_d = components.aggregate(Sum('weightage_d'))
    total_weightage_element_a = elements.aggregate(Sum('weightage_a'))
    total_weightage_element_b = elements.aggregate(Sum('weightage_b'))
    total_weightage_element_c = elements.aggregate(Sum('weightage_c'))
    total_weightage_element_d = elements.aggregate(Sum('weightage_d'))
    tw_a = 0
    tw_b = 0
    tw_c = 0
    tw_d = 0
    tw_element_a = 0
    tw_element_b = 0
    tw_element_c = 0
    tw_element_d = 0
    if total_weightage_a['weightage_a__sum'] == None:
        tw_a = 0
    else:
        tw_a = total_weightage_a['weightage_a__sum']
    if total_weightage_b['weightage_b__sum'] == None:
        tw_b = 0
    else:
        tw_b = total_weightage_b['weightage_b__sum']
    if total_weightage_c['weightage_c__sum'] == None:
        tw_c = 0
    else:
        tw_c = total_weightage_c['weightage_c__sum']
    if total_weightage_d['weightage_d__sum'] == None:
        tw_d = 0
    else:
        tw_d = total_weightage_d['weightage_d__sum']
    if total_weightage_element_a['weightage_a__sum'] == None:
        tw_element_a = 0
    else:
        tw_element_a = total_weightage_element_a['weightage_a__sum']
    if total_weightage_element_b['weightage_b__sum'] == None:
        tw_element_b = 0
    else:
        tw_element_b = total_weightage_element_b['weightage_b__sum']
    if total_weightage_element_c['weightage_c__sum'] == None:
        tw_element_c = 0
    else:
        tw_element_c = total_weightage_element_c['weightage_c__sum']
    if total_weightage_element_d['weightage_d__sum'] == None:
        tw_element_d = 0
    else:
        tw_element_d = total_weightage_element_d['weightage_d__sum']
    form = ComponentCreateForm()
    context = {
        'mode':'component',
        'title': 'Components',
        'form': form,
        'total_weightage_a':tw_a + tw_element_a,
        'total_weightage_b':tw_b + tw_element_b,
        'total_weightage_c':tw_c + tw_element_c,
        'total_weightage_d':tw_d + tw_element_d,
        'components':components,
        'elements':elements,
    }

    if request.method == 'POST':
        form = ComponentCreateForm(request.POST)
        if form.is_valid():
            form_data = form.save()
            form_data.created_by = request.user.name
            form_data.modified_by = request.user.name
            form_data.save()
            messages.info(request,'Successfully created new component')
        else:
            messages.warning(request,'Error creating new component')
        return redirect('dashboard_manage_component_v2')
    return render(request, "dashboard/management/manage_component_v2.html", context)

@login_required(login_url="/login/")
@allowed_users(allowed_roles=['superadmin'])
def dashboard_manage_sub_component_v2(request, mode, id):
    parent = None
    total_weightage = 0
    children = None
    title = ''
    form = None
    check_loop = None
    if mode == 'sub_component':
        parent = get_object_or_404(Component,id=id)
        children = SubComponent.objects.all().filter(component=parent)
        
        for child in children:
            total_weightage += child.get_total_weightage()
            
        form = SubComponentCreateForm()
        title = 'Sub Components'
    if mode == 'element':
        parent = get_object_or_404(SubComponent,id=id)
        children = Element.objects.all().filter(sub_component=parent)
        form = ElementCreateForm()
        title = 'Elements'
    if mode == 'defect_group':
        parent = get_object_or_404(Element,id=id)
        children = DefectGroup.objects.all().filter(element=parent)
        form = DefectGroupCreateForm()
        title = 'Defect Groups'
        check_loop = range(parent.no_of_check)
    context = {
        'mode':mode,
        'parent':parent,
        'children':children,
        # 'special_elements':special_elements,
        'title': title,
        'form': form,
        'total_weightage':total_weightage,
        'check_loop': check_loop
    }

    if request.method == 'POST':
        if mode == 'sub_component':
            form = SubComponentCreateForm(request.POST)
        if mode == 'element':
            form = ElementCreateForm(request.POST)
        if mode == 'defect_group':
            form = DefectGroupCreateForm(request.POST)
        if form.is_valid():
            form_data = form.save()
            form_data.created_by = request.user.name
            form_data.modified_by = request.user.name
            if mode == 'sub_component':
                form_data.component = parent
                messages.info(request,'Successfully created new sub component')
            if mode == 'element':
                form_data.sub_component = parent
                messages.info(request,'Successfully created new element')
            if mode == 'defect_group':
                form_data.element = parent
                messages.info(request,'Successfully created new defect group')
            form_data.save()
        else:
            messages.warning(request,'Problem creating a new entry')
        return redirect('dashboard_manage_sub_component_v2', mode, parent.id)
    return render(request, "dashboard/management/manage_component_v2.html", context)

from assessments.forms import (
    ComponentEditForm,
    SubComponentEditForm,
    ElementEditForm,
    DefectGroupEditForm,
    # ElementWithWeightageEditForm,
)

@login_required(login_url="/login/")
@allowed_users(allowed_roles=['superadmin'])
def dashboard_manage_edit_component_v2(request, mode, id):
    children = None
    parent = None
    form = None
    title=''
    if mode == 'component':
        children = get_object_or_404(Component,id=id)
        form = ComponentEditForm(instance=children)
        title = 'Component'
    if mode == 'sub_component':
        children = get_object_or_404(SubComponent,id=id)
        parent = children.component
        form = SubComponentEditForm(instance=children)
        title = 'Sub Component'
    if mode == 'element':
        children = get_object_or_404(Element,id=id)
        parent = children.sub_component
        # if children.sub_component_weightage == True:
        #     form = ElementWithWeightageEditForm(instance=children)
        # else:
        form = ElementEditForm(instance=children)
        title = 'Element'
    if mode == 'defect_group':
        children = get_object_or_404(DefectGroup,id=id)
        parent = children.element
        form = DefectGroupEditForm(instance=children)
        title = 'Defect Group'
    context = {
        'mode':mode,
        'form':form,
        'children':children,
        'title':title,
        'parent':parent,
    }

    if request.method == 'POST':
        if 'update' in request.POST:
            if mode == 'component':
                form = ComponentEditForm(request.POST, instance=children)
            elif mode == 'sub_component':
                form = SubComponentEditForm(request.POST, instance=children)
            elif mode == 'element':
                # if children.sub_component_weightage == True:
                #     form = ElementWithWeightageEditForm(request.POST, instance=children)
                # else:
                form = ElementEditForm(request.POST, instance=children)
            elif mode == 'defect_group':
                form = DefectGroupEditForm(request.POST, instance=children)
            else:
                pass
            if form.is_valid():
                form_data = form.save()
                form_data.modified_by = request.user.name
                form_data.save()
                messages.info(request,'Updated successfully')
            else:
                messages.warning(request,'Problem updating the data')
            return redirect('dashboard_manage_edit_component_v2', mode, children.id)
        if 'delete' in request.POST:
            parent_id = ''
            if mode == 'sub_component':
                parent_id = parent.id
            if mode == 'element':
                parent_id = parent.id
            if mode == 'defect_group':
                parent_id = parent.id
            children.delete()
            messages.info(request,'Successfully deleted the data')
            
            if mode == 'component':
                return redirect('dashboard_manage_component_v2')
            return redirect('dashboard_manage_sub_component_v2', mode, parent_id)
    return render(request, "dashboard/management/manage_component_edit_v2.html", context)
