# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

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

# Forms
from assessments.forms import DefectGroupCreateForm, SubComponentCreateForm, ElementCreateForm, ComponentCreateForm
from projects.forms import VerifiedContractorForm
from portal.forms import LetterTemplateCreateForm
from trainings.forms import TrainingTypeCreateForm

# Models
from assessments.models import DefectGroup, SubComponent, Element, Component, QlassicAssessmentApplication
from trainings.models import TrainingType
from projects.models import ProjectInfo, VerifiedContractor
from portal.models import Announcement, Publication, Training, LetterTemplate

# Generate Document
from core.helpers import translate_malay_date, standard_date
from app.helpers.letter_templates import generate_document

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
    trainings = Training.objects.all()
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

@login_required(login_url="/login/")
def view_pdf(request):
    qaa = QlassicAssessmentApplication.objects.all().order_by('-id')[0]
    context = {
        'qaa': qaa
    }
    return render(request, "pdf/score_letter.html", context)

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
@allowed_users(allowed_roles=['superadmin'])
@login_required(login_url="/login/")
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

@allowed_users(allowed_roles=['superadmin'])
@login_required(login_url="/login/")
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

@allowed_users(allowed_roles=['superadmin'])
@login_required(login_url="/login/")
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

@allowed_users(allowed_roles=['superadmin'])
@login_required(login_url="/login/")
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

@allowed_users(allowed_roles=['superadmin'])
@login_required(login_url="/login/")
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

@allowed_users(allowed_roles=['superadmin'])
@login_required(login_url="/login/")
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

@allowed_users(allowed_roles=['superadmin'])
@login_required(login_url="/login/")
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

@allowed_users(allowed_roles=['superadmin'])
@login_required(login_url="/login/")
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

@allowed_users(allowed_roles=['superadmin'])
@login_required(login_url="/login/")
def dashboard_management_letter_id(request, id):
    context = {
    }
    return render(request, "dashboard/management/letter_id.html", context)

@allowed_users(allowed_roles=['superadmin'])
@login_required(login_url="/login/")
def dashboard_management_letter(request):
    context = {
    }
    return render(request, "dashboard/management/letter.html", context)

@allowed_users(allowed_roles=['superadmin'])
@login_required(login_url="/login/")
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

@allowed_users(allowed_roles=['superadmin'])
@login_required(login_url="/login/")
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

@allowed_users(allowed_roles=['superadmin'])
@login_required(login_url="/login/")
def dashboard_letter_template(request):
    letter_templates = LetterTemplate.objects.all()
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
                messages.warning(request, 'Unable to create new letter template')
        if 'test_template' in request.POST:
            id = request.POST['id']
            template_type = request.POST['template_type']
            response = test_letter_template(id, template_type)
            return response

        return redirect('dashboard_letter_template')
    context = {"letter_templates": letter_templates, 'form_letter_template': form_letter_template}
    return render(request, "dashboard/management/letter_template.html", context)

@allowed_users(allowed_roles=['superadmin'])
@login_required(login_url="/login/")
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

@allowed_users(allowed_roles=['superadmin'])
@login_required(login_url="/login/")
def dashboard_training_type(request):
    training_types = TrainingType.objects.all()
    form_training_type = TrainingTypeCreateForm()
    if request.method == 'POST':
        if 'create' in request.POST:
            form_training_type = TrainingTypeCreateForm(request.POST,request.FILES)
            if form_training_type.is_valid():
                form_training_type.save()
                messages.info(request, 'Created successfully')
            else:
                messages.warning(request, 'Unable to create new training type')

        return redirect('dashboard_training_type')
    context = {"training_types": training_types, 'form_training_type': form_training_type}
    return render(request, "dashboard/management/training_type.html", context)

@allowed_users(allowed_roles=['superadmin'])
@login_required(login_url="/login/")
def dashboard_training_type_id(request, id):
    training_type = get_object_or_404(TrainingType, id=id)
    form_training_type = TrainingTypeCreateForm(instance=training_type)
    if request.method == 'POST':
        if 'delete' in request.POST:
            training_type.delete()
            messages.info(request, 'Deleted successfully')
            return redirect('dashboard_training_type')
        if 'update' in request.POST:
            form_training_type = TrainingTypeCreateForm(request.POST,request.FILES,instance=training_type)
            if form_training_type.is_valid():
                form_training_type.save()
                messages.info(request, 'Updated successfully')
            else:
                messages.warning(request, 'Unable to update training_type')

        return redirect('dashboard_training_type_id', id)
    context = {"training_type": training_type,'form_training_type':form_training_type}
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