# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.http import Http404, HttpResponse, JsonResponse
from django.db.models import Q
import datetime
import random

# Payment
from django.views.decorators.csrf import csrf_exempt
from api.soap.create_transaction import create_transaction, payment_gateway_url, get_receipt_url
from billings.helpers import payment_response_process, get_payment_history_url
from billings.models import Payment

import requests

from core.helpers import get_state_code, get_sector_code, send_email_default, get_domain

# Forms
from users.forms import UserUpdateForm
from assessments.forms import QAACreateForm, QAAApplicationForm, QAAReviewForm, QAAVerifyForm, SupportingDocumentsUploadForm
from projects.forms import ProjectInfoCreateForm, ProjectInfoApplicationForm

# Models
from users.models import Assessor, CustomUser
from projects.models import Contractor, VerifiedContractor, ProjectInfo
from assessments.models import (
    Component, ElementResult, SampleResult, 
    SubComponent, 
    Element, 
    DefectGroup, 
    QlassicAssessmentApplication, 
    SupportingDocuments, 
    SuggestedAssessor, 
    AssignedAssessor, 
    AssessmentData
)

# SOAP
from api.soap.get_contractor import get_project, verify_contractor

# Decorators
from authentication.decorators import allowed_users

### Admin - Application Module ###
@login_required(login_url="/login/")
def dashboard_application_overview(request):
    return render(request, "dashboard/application/overview.html")

@login_required(login_url="/login/")
@allowed_users(allowed_roles=['superadmin'])
def dashboard_application(request):
    return render(request, "dashboard/application/list.html")

@login_required(login_url="/login/")
@allowed_users(allowed_roles=['contractor'])
def dashboard_application_profile(request):
    user = request.user
    form_user = UserUpdateForm(instance=user)
    if request.method == 'POST':
        form_user = UserUpdateForm(request.POST, request.FILES or None, instance=user)
        if form_user.is_valid():
            form_user.save()
            messages.info(request, 'Updated successfully')
        else:
            messages.warning(request, 'Unable to update profile')
        return redirect('dashboard_application_profile')
    context = { 'form_user': form_user}
    return render(request, "dashboard/application/profile.html", context)

# @login_required(login_url="/login/")
# def dashboard_application_project(request):
    
#     contractors = Contractor.objects.all().filter(qaa_number=None)
    
#     # GET Filter
#     sector = ''
#     if 'sector' in request.GET:
#         sector = request.GET['sector']
#         if filter != '':
#             contractors = contractors.filter(project_type=sector)

#     context = {
#         'sector':sector,
#         'contractors':contractors,
#     }
#     return render(request, "dashboard/application/project_list.html", context)

@login_required(login_url="/login/")
@allowed_users(allowed_roles=['superadmin','contractor','applicant'])
def dashboard_application_project(request):
    # Check if verified contractor before displaying the list of contractor
    verified_contractor = VerifiedContractor.objects.filter(user=request.user,is_verified=True).first()
    contractors = None
    require_verification = False
    if verified_contractor == None:
        require_verification = True
    else:
        contractors = get_project(verified_contractor.contractor_registration_number)

    # GET Filter
    sector = ''
    if 'sector' in request.GET:
        sector = request.GET['sector']
        if sector != '':
            contractors = contractors.filter(project_type=sector)

    context = {
        'verified_contractor':verified_contractor,
        'require_verification':require_verification,
        'sector':sector,
        'contractors':contractors,
    }

    if request.method == 'POST':
        ssm_number = request.POST['ssm_number']
        contractor_registration_number = request.POST['contractor_registration_number']
        is_verify = verify_contractor(contractor_registration_number)
        if is_verify:
            VerifiedContractor.objects.create(
                user = request.user,
                ssm_number = ssm_number,
                contractor_registration_number = contractor_registration_number,
                is_verified = True,
                created_by = request.user.name,
                modified_by = request.user.name,
            )
            messages.info(request, 'Successfully verify the contractor profile')
        else:
            messages.warning(request, 'Record not found. Failed to verify the contractor. Please correct your details to verify again.')
        return redirect('dashboard_application_project')

    return render(request, "dashboard/application/project_list.html", context)

@login_required(login_url="/login/")
@allowed_users(allowed_roles=['superadmin','contractor','applicant'])
def dashboard_application_new(request, contractor_registration_number, id):
    contractor = get_object_or_404(Contractor, contractor_registration_number=contractor_registration_number, project_reference_number=id)
    qaa = None
    pi = None
    create_new_qaa = False
    qaa_all = QlassicAssessmentApplication.objects.filter(pi__contractor_cidb_registration_no=contractor_registration_number, pi__project_reference_number=id).order_by('-created_date')
    # qaa_all = QlassicAssessmentApplication.objects.all().filter(contractor=contractor).order_by('-created_date')
    if qaa_all.count() > 0:
        qaa = qaa_all[0]
        pi = qaa.pi
        if qaa.application_status == 'rejected':
            create_new_qaa = True
        elif qaa.application_status == 'rejected_amendment' or qaa.application_status == None or qaa.application_status == '':
            qaa = qaa
        else:
            messages.warning(request, 'Unable to apply QLASSIC. This project is already been registered in QLASSIC ASSESSMENT APPLICATION')
            return redirect('dashboard_application_project')  
        
        if pi == None:
            pi = ProjectInfo.objects.create()
            qaa.pi=pi
            qaa.save()
    else:
        create_new_qaa = True
    
    if create_new_qaa:
        print('created new qaa and pi')
        pi = ProjectInfo.objects.create()
        qaa = QlassicAssessmentApplication.objects.create(user=request.user, pi=pi)

    # Refresh new information
    # pi.project_type = contractor.project_type
    pi.levy_number = contractor.levy_number
    pi.project_title = contractor.project_title
    pi.project_reference_number = contractor.project_reference_number
    pi.contractor_name = contractor.name_of_contractor
    pi.contractor_cidb_registration_no = contractor.contractor_registration_number
    pi.contractor_registration_grade = contractor.contractor_registration_grade
    pi.contract_value = contractor.contract_value
    pi.project_location = contractor.project_location
    pi.save()
    qaa.applicant_name = request.user.name
    qaa.role = request.user.role
    qaa.organization = request.user.organization
    qaa.address1 = request.user.address1
    qaa.address2 = request.user.address2
    qaa.city = request.user.city
    qaa.state = request.user.state
    qaa.postcode = request.user.postcode
    qaa.email = request.user.email
    qaa.hp_no = request.user.hp_no
    qaa.fax_no = request.user.fax_no
    qaa.save()

    assessment_data, created = AssessmentData.objects.get_or_create(qaa=qaa)
        
    form_qaa = QAACreateForm(instance=qaa)
    if request.method == 'POST':
        form_qaa = QAAApplicationForm(request.POST,instance=qaa)
        if form_qaa.is_valid():
            qaa = form_qaa.save()
            messages.info(request,'Successfully save')
            return redirect('dashboard_application_new_2', contractor.contractor_registration_number, contractor.project_reference_number)
        else:
            messages.warning(request,'Problem with details'+form_qaa.errors.as_text())
            return redirect('dashboard_application_new', contractor.contractor_registration_number, contractor.project_reference_number)

    #     if contractor.qaa_number == None:
            
            
    #         qaa = QlassicAssessmentApplication.objects.get_or_create(
    #             first_name='John',
    #             last_name='Lennon',
    #             defaults={'birthday': date(1940, 10, 9)},
    #         )
    context = {'qaa':qaa, 'form_qaa':form_qaa, 'contractor':contractor}
    return render(request, "dashboard/application/application_form_1.html",context)

@login_required(login_url="/login/")
def dashboard_application_new_2(request, contractor_registration_number, id):
    contractor = get_object_or_404(Contractor, contractor_registration_number=contractor_registration_number, project_reference_number=id)
    qaa = QlassicAssessmentApplication.objects.filter(pi__contractor_cidb_registration_no=contractor_registration_number, pi__project_reference_number=id).order_by('-created_date')[0]
    pi = qaa.pi

    form_pi = ProjectInfoCreateForm(instance=pi)
    if request.method == 'POST':
        form_pi = ProjectInfoApplicationForm(request.POST, request.FILES, instance=pi)
        if form_pi.is_valid():
            pi_submit = form_pi.save()
            if pi_submit.project_type == 'GOVERNMENT':
                qaa.payment_mode = 'off'
            else:
                qaa.payment_mode = 'on'
            qaa.save()
            messages.info(request,'Successfully save')

            return redirect('dashboard_application_new_3', contractor.contractor_registration_number, contractor.project_reference_number)
        else:
            messages.warning(request,'Problem with details'+form_pi.errors.as_text())
            return redirect('dashboard_application_new_2', contractor.contractor_registration_number, contractor.project_reference_number)

    context = {'pi':pi,'form_pi':form_pi, 'contractor':contractor}
    return render(request, "dashboard/application/application_form_2.html",context)


@login_required(login_url="/login/")
def dashboard_application_new_3(request, contractor_registration_number, id):
    contractor = get_object_or_404(Contractor, contractor_registration_number=contractor_registration_number, project_reference_number=id)
    qaa = QlassicAssessmentApplication.objects.filter(pi__contractor_cidb_registration_no=contractor_registration_number, pi__project_reference_number=id).order_by('-created_date')[0]
    pi = qaa.pi

    print(generate_qaa_number(qaa))

    sd = SupportingDocuments.objects.all().filter(qaa=qaa)
    sd_1, created = sd.get_or_create(qaa=qaa, file_name='sd_1')
    sd_2, created = sd.get_or_create(qaa=qaa, file_name='sd_2')
    sd_3, created = sd.get_or_create(qaa=qaa, file_name='sd_3')
    sd_4, created = sd.get_or_create(qaa=qaa, file_name='sd_4')
    sd_5, created = sd.get_or_create(qaa=qaa, file_name='sd_5')
    sd_6, created = sd.get_or_create(qaa=qaa, file_name='sd_6')
    sd_7, created = sd.get_or_create(qaa=qaa, file_name='sd_7')
    sd_8, created = sd.get_or_create(qaa=qaa, file_name='sd_8')
    sd_9, created = sd.get_or_create(qaa=qaa, file_name='sd_9')
    context = {
        'contractor':contractor,
        'sd_1':sd_1,
        'sd_2':sd_2,
        'sd_3':sd_3,
        'sd_4':sd_4,
        'sd_5':sd_5,
        'sd_6':sd_6,
        'sd_7':sd_7,
        'sd_8':sd_8,
        'sd_9':sd_9
    }
    if request.method == 'POST':
        form_sd = SupportingDocumentsUploadForm(request.POST,request.FILES)
        if form_sd.is_valid():
            data_sd_1 = form_sd.cleaned_data.get('sd_1')
            data_sd_2 = form_sd.cleaned_data.get('sd_2')
            data_sd_3 = form_sd.cleaned_data.get('sd_3')
            data_sd_4 = form_sd.cleaned_data.get('sd_4')
            data_sd_5 = form_sd.cleaned_data.get('sd_5')
            data_sd_6 = form_sd.cleaned_data.get('sd_6')
            data_sd_7 = form_sd.cleaned_data.get('sd_7')
            data_sd_8 = form_sd.cleaned_data.get('sd_8')
            data_sd_9 = form_sd.cleaned_data.get('sd_9')
            if data_sd_1 != None:
                sd_1.file = data_sd_1
                sd_1.save()
            if data_sd_2 != None:
                sd_2.file = data_sd_2
                sd_2.save()
            if data_sd_3 != None:
                sd_3.file = data_sd_3
                sd_3.save()
            if data_sd_4 != None:
                sd_4.file = data_sd_4
                sd_4.save()
            if data_sd_5 != None:
                sd_5.file = data_sd_5
                sd_5.save()
            if data_sd_6 != None:
                sd_6.file = data_sd_6
                sd_6.save()
            if data_sd_7 != None:
                sd_7.file = data_sd_7
                sd_7.save()
            if data_sd_8 != None:
                sd_8.file = data_sd_8
                sd_8.save()
            if data_sd_9 != None:
                sd_9.file = data_sd_9
                sd_9.save()
            
            # Change status to pending
            qaa.application_status = 'pending'
            
            # Generate QAA Number
            # if qaa.qaa_number == None or qaa.qaa_number == '':
            #     qaa_count = ProjectInfo.objects.filter(project_location=pi.project_location,qaa__building_type=qaa.building_type,project_type=pi.project_type).exclude(qaa__qaa_number='').count()
            #     qaa_number = ''
            #     new_number = False
            #     while new_number==False:
            #         qaa_count += 1
            #         print(contractor.project_type)
            #         qaa_number = get_state_code(pi.project_location) + datetime.datetime.now().strftime('%y') + ' ' + qaa.building_type + 'P' + str(qaa_count).zfill(4) + " C (" + get_sector_code(pi.project_type) + ")"
            #         check_qaa_exist = QlassicAssessmentApplication.objects.all().filter(qaa_number=qaa_number)
            #         if check_qaa_exist.count() == 0:
            #             new_number=True
            #     qaa.qaa_number = qaa_number
            if qaa.qaa_number == None or qaa.qaa_number == '':
                qaa_number = generate_qaa_number(qaa)
                qaa.qaa_number = qaa_number

            qaa.created_date = datetime.datetime.now()
            qaa.save()

            messages.info(request,'QLASSIC Assessment Application completed')

            # Email send to User
            subject = 'QLASSIC Assessment Application are being Processed ('+ qaa.qaa_number +')'
            context = {
                'qaa': qaa,
                'user': request.user,
            }
            to = [request.user.email]
            send_email_default(subject, to, context, 'email/qaa-sent.html')
            
            # Email send to reviewer
            reviewers = CustomUser.objects.all().filter(
                Q(role='casc_reviewer')|
                Q(role='superadmin')
            )
            to = []
            context = {
                'qaa': qaa
            }
            for rev in reviewers:
                to.append(rev.email)
            subject = 'New QLASSIC Assessment Application to be reviewed ('+ qaa.qaa_number +')'
            send_email_default(subject, to, context, 'email/qaa-sent-reviewer.html')

            return redirect('dashboard_application_list')
        else:
            messages.warning(request, 'Problem with uploading the documents: '+form_sd.errors.as_text())
        return redirect('dashboard_application_new_3', contractor.contractor_registration_number, contractor.project_reference_number)

    return render(request, "dashboard/application/application_form_3.html",context)

def generate_qaa_number(qaa):

    # Get list of all applied project
    project_applied = QlassicAssessmentApplication.objects.all().exclude(
        Q(qaa_number='')|
        Q(qaa_number=None)
    )

    # Find project that match with current project
    current_year = datetime.datetime.now().strftime('%Y')
    fil = project_applied.filter(
        pi__created_date__year=current_year,
        pi__project_location= qaa.pi.project_location,
        building_type= qaa.building_type,
        pi__project_type= qaa.pi.project_type,
    )

    qaa_number = ''
    count = len(fil)
    new_number=False

    #Generate QAA unique number
    while new_number==False:
        count += 1
        qaa_number = get_state_code(qaa.pi.project_location) + datetime.datetime.now().strftime('%y') + ' ' + qaa.building_type + 'P' + str(count).zfill(4) + " C (" + get_sector_code(qaa.pi.project_type) + ")"
        check_qaa_exist = project_applied.filter(qaa_number=qaa_number)
        if check_qaa_exist.count() == 0:
            new_number=True
    return qaa_number

@login_required(login_url="/login/")
def dashboard_application_info(request, id):
    mode = ''

    qaa = get_object_or_404(QlassicAssessmentApplication, id=id)
    sd = SupportingDocuments.objects.all().filter(qaa=qaa)
    sd_1, created = sd.get_or_create(qaa=qaa, file_name='sd_1')
    sd_2, created = sd.get_or_create(qaa=qaa, file_name='sd_2')
    sd_3, created = sd.get_or_create(qaa=qaa, file_name='sd_3')
    sd_4, created = sd.get_or_create(qaa=qaa, file_name='sd_4')
    sd_5, created = sd.get_or_create(qaa=qaa, file_name='sd_5')
    sd_6, created = sd.get_or_create(qaa=qaa, file_name='sd_6')
    sd_7, created = sd.get_or_create(qaa=qaa, file_name='sd_7')
    sd_8, created = sd.get_or_create(qaa=qaa, file_name='sd_8')
    sd_9, created = sd.get_or_create(qaa=qaa, file_name='sd_9')
    context = {
        'mode': mode,
        'qaa':qaa,
        'sd_1':sd_1,
        'sd_2':sd_2,
        'sd_3':sd_3,
        'sd_4':sd_4,
        'sd_5':sd_5,
        'sd_6':sd_6,
        'sd_7':sd_7,
        'sd_8':sd_8,
        'sd_9':sd_9,
    }
        
    return render(request, "dashboard/application/application_info.html", context)

@login_required(login_url="/login/")
def dashboard_application_info_assessor(request, id, assessor_mode):
    mode = ''

    qaa = get_object_or_404(QlassicAssessmentApplication, id=id)
    sd = SupportingDocuments.objects.all().filter(qaa=qaa)
    sd_1, created = sd.get_or_create(qaa=qaa, file_name='sd_1')
    sd_2, created = sd.get_or_create(qaa=qaa, file_name='sd_2')
    sd_3, created = sd.get_or_create(qaa=qaa, file_name='sd_3')
    sd_4, created = sd.get_or_create(qaa=qaa, file_name='sd_4')
    sd_5, created = sd.get_or_create(qaa=qaa, file_name='sd_5')
    sd_6, created = sd.get_or_create(qaa=qaa, file_name='sd_6')
    sd_7, created = sd.get_or_create(qaa=qaa, file_name='sd_7')
    sd_8, created = sd.get_or_create(qaa=qaa, file_name='sd_8')
    sd_9, created = sd.get_or_create(qaa=qaa, file_name='sd_9')
    context = {
        'mode': mode,
        'assessor_view': True,
        'assessor_mode': assessor_mode,
        'qaa':qaa,
        'sd_1':sd_1,
        'sd_2':sd_2,
        'sd_3':sd_3,
        'sd_4':sd_4,
        'sd_5':sd_5,
        'sd_6':sd_6,
        'sd_7':sd_7,
        'sd_8':sd_8,
        'sd_9':sd_9,
    }
        
    return render(request, "dashboard/application/application_info.html", context)

@login_required(login_url="/login/")
def dashboard_application_review(request, id):
    mode = 'review'

    qaa = get_object_or_404(QlassicAssessmentApplication, id=id)
    form_review = QAAReviewForm(instance=qaa)
    sd = SupportingDocuments.objects.all().filter(qaa=qaa)
    sd_1, created = sd.get_or_create(qaa=qaa, file_name='sd_1')
    sd_2, created = sd.get_or_create(qaa=qaa, file_name='sd_2')
    sd_3, created = sd.get_or_create(qaa=qaa, file_name='sd_3')
    sd_4, created = sd.get_or_create(qaa=qaa, file_name='sd_4')
    sd_5, created = sd.get_or_create(qaa=qaa, file_name='sd_5')
    sd_6, created = sd.get_or_create(qaa=qaa, file_name='sd_6')
    sd_7, created = sd.get_or_create(qaa=qaa, file_name='sd_7')
    sd_8, created = sd.get_or_create(qaa=qaa, file_name='sd_8')
    sd_9, created = sd.get_or_create(qaa=qaa, file_name='sd_9')
    context = {
        'mode': mode,
        'qaa':qaa,
        'form_review':form_review,
        'sd_1':sd_1,
        'sd_2':sd_2,
        'sd_3':sd_3,
        'sd_4':sd_4,
        'sd_5':sd_5,
        'sd_6':sd_6,
        'sd_7':sd_7,
        'sd_8':sd_8,
        'sd_9':sd_9,
    }
    if request.method == 'POST':
        if 'reject' in request.POST or 'reject_amendment' in request.POST:
            if 'reject' in request.POST:
                qaa.application_status = 'rejected'
                messages.info(request,'Successfully rejected the application')
            if 'reject_amendment' in request.POST:
                qaa.application_status = 'rejected_amendment'
                messages.info(request,'Successfully rejected (with amendment) the application')
            
            qaa.remarks1 = request.POST['remarks1']
            qaa.reviewed_by = request.user.name
            qaa.reviewed_date = datetime.datetime.now()

            # Clear the previous verifier remarks
            qaa.remarks2 = None
            qaa.verified_by = None
            qaa.verified_date = None
            qaa.save()

            # Email send to User
            subject = 'QLASSIC Assessment Application are being rejected ('+ qaa.qaa_number +')'
            context = {
                'qaa': qaa,
                'user': request.user,
            }
            to = [request.user.email]
            send_email_default(subject, to, context, 'email/qaa-rejected.html')

            return redirect('dashboard_application_list')
        if 'accept' in request.POST:
            form_review = QAAReviewForm(request.POST, instance=qaa)
            if form_review.is_valid():
                form_review.save()
                qaa.reviewed_by = request.user.name
                qaa.reviewed_date = datetime.datetime.now()
                
                qaa.remarks2 = None
                qaa.verified_by = None
                qaa.verified_date = None

                qaa.application_status = 'reviewed'
                qaa.save()

                messages.info(request,'Successfully reviewed the application')

                # Email send to verifier
                verifiers = CustomUser.objects.all().filter(
                    Q(role='casc_verifier')|
                    Q(role='superadmin')
                )
                to = []
                context = {
                    'qaa': qaa
                }
                for ver in verifiers:
                    to.append(ver.email)
                subject = 'New QLASSIC Assessment Application to be verified ('+ qaa.qaa_number +')'
                send_email_default(subject, to, context, 'email/qaa-sent-verifier.html')

                return redirect('dashboard_application_list')
            else:
                messages.warning(request,'Problem with reviewing the application:'+form_review.errors.as_text())
                return redirect('dashboard_application_review', qaa.id)
        
    return render(request, "dashboard/application/application_info.html", context)

@login_required(login_url="/login/")
def dashboard_application_verify(request, id):
    mode = 'verify'

    qaa = get_object_or_404(QlassicAssessmentApplication, id=id)

    form_verify = QAAVerifyForm(instance=qaa)
    sd = SupportingDocuments.objects.all().filter(qaa=qaa)
    sd_1, created = sd.get_or_create(qaa=qaa, file_name='sd_1')
    sd_2, created = sd.get_or_create(qaa=qaa, file_name='sd_2')
    sd_3, created = sd.get_or_create(qaa=qaa, file_name='sd_3')
    sd_4, created = sd.get_or_create(qaa=qaa, file_name='sd_4')
    sd_5, created = sd.get_or_create(qaa=qaa, file_name='sd_5')
    sd_6, created = sd.get_or_create(qaa=qaa, file_name='sd_6')
    sd_7, created = sd.get_or_create(qaa=qaa, file_name='sd_7')
    sd_8, created = sd.get_or_create(qaa=qaa, file_name='sd_8')
    sd_9, created = sd.get_or_create(qaa=qaa, file_name='sd_9')
    context = {
        'mode': mode,
        'qaa':qaa,
        'form_verify':form_verify,
        'sd_1':sd_1,
        'sd_2':sd_2,
        'sd_3':sd_3,
        'sd_4':sd_4,
        'sd_5':sd_5,
        'sd_6':sd_6,
        'sd_7':sd_7,
        'sd_8':sd_8,
        'sd_9':sd_9,
    }
    if request.method == 'POST':
        if 'reject' in request.POST or 'reject_amendment' in request.POST:
            if 'reject' in request.POST:
                qaa.application_status = 'rejected'
                messages.info(request,'Successfully rejected the application')
            if 'reject_amendment' in request.POST:
                qaa.application_status = 'rejected_amendment'
                messages.info(request,'Successfully rejected (with amendment) the application')
            qaa.remarks2 = request.POST['remarks2']
            qaa.verified_by = request.user.name
            qaa.verified_date = datetime.datetime.now()
            qaa.save()

            # Email send to User
            subject = 'QLASSIC Assessment Application are being rejected ('+ qaa.qaa_number +')'
            context = {
                'qaa': qaa,
                'user': request.user,
            }
            to = [request.user.email]
            send_email_default(subject, to, context, 'email/qaa-rejected.html')

            return redirect('dashboard_application_list')
        if 'accept' in request.POST:
            form_verify = QAAVerifyForm(request.POST, instance=qaa)
            if form_verify.is_valid():
                form_verify.save()
                qaa.verified_by = request.user.name
                qaa.verified_date = datetime.datetime.now()
                if qaa.payment_mode == 'off':
                    qaa.application_status = 'verified'

                    # Email CASC Verifier
                    verifiers = CustomUser.objects.all().filter(
                        Q(role='casc_verifier')|
                        Q(role='superadmin')
                    )
                    to = []
                    for verifier in verifiers:
                        to.append(verifier.email)
                    subject = "Assessor Assignation - " + qaa.qaa_number
                    ctx_email = {
                        'qaa':qaa,
                    }
                    send_email_default(subject, to, ctx_email, 'email/qaa-verified.html')
                else:
                    qaa.application_status = 'need_payment'
                qaa.save()

                # Remove current suggestion
                assessors = SuggestedAssessor.objects.all().filter(qaa=qaa)
                assessors.delete()

                # Create suggested assessor based on value set by verifier and assign the assessor randomly
                sas = SuggestedAssessor.objects.all().filter(qaa=qaa)
                i = 0
                ass_list = list(Assessor.objects.all())
                random.shuffle(ass_list)
                for x in range(qaa.no_of_assessor):
                    sa = SuggestedAssessor.objects.create(qaa=qaa)
                    if i < len(ass_list):
                        print(ass_list[i])
                        sa.assessor = ass_list[i]
                        sa.assessor_no = ass_list[i].assessor_no
                        sa.save()
                    i = i + 1

                messages.info(request,'Successfully verified the application')
                return redirect('dashboard_application_list')
            else:
                messages.warning(request,'Problem with verifying the application:'+form_verify.errors.as_text())
                return redirect('dashboard_application_verify', qaa.id)
    return render(request, "dashboard/application/application_info.html", context)

@login_required(login_url="/login/")
def dashboard_application_list(request):
    qaas = None
    role_display_staff = [
        'superadmin',
        'casc_reviewer',
        'casc_verifier',
        'cidb_verifier',
    ]
    role_display_applicant = [
        'contractor',
        'applicant',
    ]
    
    role_type = ''
    if request.user.role in role_display_staff:
        role_type = 'staff'
        qaas = QlassicAssessmentApplication.objects.all().order_by('-created_date')
    elif request.user.role in role_display_applicant:
        role_type = 'applicant'
        qaas = QlassicAssessmentApplication.objects.all().filter(user=request.user).order_by('-created_date')
    else:
        messages.warning(request, 'You are not eligible to view the list of applications.')
        qaas = None
    
    # GET Filter
    sector = ''
    if qaas != None:
        if 'sector' in request.GET:
            sector = request.GET['sector']
            if sector != '':
                qaas = qaas.filter(pi__project_type=sector)

    context = {
        'role_type':role_type,
        'sector':sector,
        'qaas':qaas,
        'payment_history_url':get_payment_history_url(request),
    }
    
    if request.method == 'POST':
        if 'reapply' in request.POST:
            # id = request.POST['id']
            contractor_cidb_registration_no = request.POST['contractor_cidb_registration_no']
            project_reference_number = request.POST['project_reference_number']
            # contractor = Contractor.objects.get(id=id)
            # return redirect('dashboard_application_new', contractor.id)
            return redirect('dashboard_application_new', contractor_cidb_registration_no, project_reference_number)

    return render(request, "dashboard/application/application_list.html",context)

# @login_required(login_url="/login/")
# def dashboard_application_payment(request, id):
#     mode = 'payment'
#     qaa = get_object_or_404(QlassicAssessmentApplication, id=id)
#     response = create_transaction(request, qaa.no_of_blocks, 'QLC', 'PERMOHONAN PENILAIAN QLASSIC', qaa.qaa_number, request.user)
#     print(response)
#     proforma = response.Code
    
#     response_url = get_domain(request) + '/dashboard/application/payment/'+id+'/response/'

#     # Create Payment
#     payment, created = Payment.objects.get_or_create(order_id=proforma)
#     payment.user = request.user
#     payment.customer_name = request.user.name
#     payment.customer_email = request.user.email
#     payment.qaa = qaa
#     payment.currency = 'MYR'
#     payment.payment_amount = response.Amount
#     payment.save()

#     context = {
#         'title': 'Payment - QLASSIC Assessment Application',
#         'mode': mode,
#         'qaa': qaa,
#         'proforma': proforma,
#         'amount': payment.payment_amount,
#         'response': response,
#         'url': payment_gateway_url,
#         'response_url': response_url,
#     }
#     return render(request, "dashboard/application/payment.html",context)

@login_required(login_url="/login/")
def dashboard_application_payment(request, id):
    mode = 'payment'
    qaa = get_object_or_404(QlassicAssessmentApplication, id=id)
    response = create_transaction(request, qaa.no_of_blocks, 'QLC', 'PERMOHONAN PENILAIAN QLASSIC', qaa.qaa_number, request.user)
    print(response)
    proforma = response.Code
    
    response_url = get_domain(request) + '/dashboard/application/payment/'+id+'/response/'

    # Create Payment
    payment, created = Payment.objects.get_or_create(order_id=proforma)
    payment.user = request.user
    payment.customer_name = request.user.name
    payment.customer_email = request.user.email
    payment.qaa = qaa
    payment.currency = 'MYR'
    payment.payment_amount = response.Amount
    payment.save()

    postdata = {
        'ClientReturnURL':response_url,
        'IcOrRoc':request.user.code_id,
        'OrderID':proforma,
        'Currency':"MYR",
        'TransactionType':"SALE",
        'ClientRef0':"",
        'ClientRef1':"",
        'ClientRef2':"",
        'ClientRef3':"",
        'ClientRef4':"",
        'Amount': payment.payment_amount,
        'CustomerName':request.user.name,
        'CustomerEmail':request.user.email,
        'CustomerPhoneNo':request.user.hp_no,
    }

    return requests.post(payment_gateway_url, data=postdata).json()

@csrf_exempt
def dashboard_application_payment_response(request, id):
    mode = 'payment_response'
    payment = None
    qaa = get_object_or_404(QlassicAssessmentApplication, id=id)
    if request.method == 'POST':
        payment = payment_response_process(request)
        if payment != None:
            if payment.payment_status == 1:
                qaa.application_status = 'verified'
                qaa.save()
                messages.info(request, 'Payment is successful. Your application will be reviewed soon.')
                
                # Email
                reviewers = CustomUser.objects.all().filter(role='casc_reviewer')
                to = []
                for reviewer in reviewers:
                    to.append(reviewer.email)
                subject = "New Transaction for QLASSIC Assessment Application - " + qaa.qaa_number
                ctx_email = {
                    'qaa':qaa,
                    'payment':payment,
                }
                send_email_default(subject, to, ctx_email, 'email/qaa-payment-response.html')
            
                # Email CASC Verifier
                verifiers = CustomUser.objects.all().filter(
                    Q(role='casc_verifier')|
                    Q(role='superadmin')
                )
                to = []
                for verifier in verifiers:
                    to.append(verifier.email)
                subject = "Assessor Assignation - " + qaa.qaa_number
                ctx_email = {
                    'qaa':qaa,
                }
                send_email_default(subject, to, ctx_email, 'email/qaa-verified.html')
            else:
                messages.warning(request, 'Payment unsuccessful. Please try again.')
        else:
            messages.warning(request, 'Problem with processing the transaction. Please contact with our staff to verify the transaction')
    receipt_url = None
    if payment != None:
        receipt_url = get_receipt_url + payment.order_id

    context = {
        'title': 'Payment Response - QLASSIC Assessment Application',
        'mode': mode,
        'training': qaa,
        'receipt_url': receipt_url,
        'payment': payment,
    }
    return render(request, "dashboard/application/payment.html",context)

@login_required(login_url="/login/")
@allowed_users(allowed_roles=['superadmin','casc_verifier','assessor'])
def dashboard_application_assessor_list(request):
    mode = 'list_all'
    context = {}
    if request.user.role == 'superadmin' or request.user.role == 'casc_verifier':
        mode = 'list_all'

    elif request.user.is_assessor:
        mode = 'list_own'
    else:
        mode = 'list_all'

    if mode == 'list_own':
        suggested_assessors = SuggestedAssessor.objects.all().filter(assessor__user=request.user).exclude(acception=None)
        context = { 
            'suggested_assessors':suggested_assessors,
            'mode':mode,
        }
    else:
        qaas = QlassicAssessmentApplication.objects.all().filter(
            Q(application_status='verified')|
            Q(application_status='assessor_assign')
        )
        suggested_assessors = SuggestedAssessor.objects.all()
        context = { 
            'qaas':qaas,
            'suggested_assessors':suggested_assessors,
            'mode':mode,
        }
    return render(request, "dashboard/application/assessor_list.html", context)

@login_required(login_url="/login/")
@allowed_users(allowed_roles=['superadmin','casc_verifier','assessor'])
def dashboard_application_assessor_list_all(request):
    mode = 'list_all'
    qaas = QlassicAssessmentApplication.objects.all().filter(
        Q(application_status='verified')|
        Q(application_status='assessor_assign')
    )
    suggested_assessors = SuggestedAssessor.objects.all()
    context = { 
        'qaas':qaas,
        'suggested_assessors':suggested_assessors,
        'mode':mode,
    }
    return render(request, "dashboard/application/assessor_list.html", context)

@login_required(login_url="/login/")
@allowed_users(allowed_roles=['superadmin','casc_verifier','assessor'])
def dashboard_application_assessor_list_own(request):
    mode = 'list_own'
    suggested_assessors = SuggestedAssessor.objects.all().filter(assessor__user=request.user).exclude(acception=None)
    context = { 
        'suggested_assessors':suggested_assessors,
        'mode':mode,
    }
   
    return render(request, "dashboard/application/assessor_list.html", context)


@login_required(login_url="/login/")
@allowed_users(allowed_roles=['superadmin','casc_verifier'])
def dashboard_application_assessor_assign(request, id):
    mode = 'assign_assessor'
    
    qaa = get_object_or_404(QlassicAssessmentApplication, id=id)
    pi = qaa.pi
    suggested_assessors = SuggestedAssessor.objects.all().filter(qaa=qaa)
    
    sd = SupportingDocuments.objects.all().filter(qaa=qaa)
    sd_1, created = sd.get_or_create(qaa=qaa, file_name='sd_1')
    sd_2, created = sd.get_or_create(qaa=qaa, file_name='sd_2')
    sd_3, created = sd.get_or_create(qaa=qaa, file_name='sd_3')
    sd_4, created = sd.get_or_create(qaa=qaa, file_name='sd_4')
    sd_5, created = sd.get_or_create(qaa=qaa, file_name='sd_5')
    sd_6, created = sd.get_or_create(qaa=qaa, file_name='sd_6')
    sd_7, created = sd.get_or_create(qaa=qaa, file_name='sd_7')
    sd_8, created = sd.get_or_create(qaa=qaa, file_name='sd_8')
    sd_9, created = sd.get_or_create(qaa=qaa, file_name='sd_9')
    context = {
        'suggested_assessors':suggested_assessors,
        'mode': mode,
        'qaa':qaa,
        'sd_1':sd_1,
        'sd_2':sd_2,
        'sd_3':sd_3,
        'sd_4':sd_4,
        'sd_5':sd_5,
        'sd_6':sd_6,
        'sd_7':sd_7,
        'sd_8':sd_8,
        'sd_9':sd_9,
    }
    if request.method == 'POST':
        assessment_data, created = AssessmentData.objects.get_or_create(qaa=qaa)
        assessment_data.user = request.user
        assessment_data.save()
        
        # Email Assigned Assessor
        to = []
        for sa in suggested_assessors:
            if sa.acception == 'accept' or sa.acception == 'pending':
                pass
            else:
                sa.acception = 'pending'
                sa.save()

            to.append(sa.assessor.user.email)
        subject = "Assessor Assignation - " + qaa.qaa_number
        ctx_email = {
            'qaa':qaa,
        }
        send_email_default(subject, to, ctx_email, 'email/qaa-assessor-assigned.html')

        qaa.save()
        messages.info(request,'Successfully assigned the assessors.')
        return redirect('dashboard_application_assessor_list_all')
    return render(request, "dashboard/application/application_info.html", context)

@login_required(login_url="/login/")
@allowed_users(allowed_roles=['superadmin','assessor'])
def dashboard_application_assessor_approve(request, id):
    mode = 'verify_assessor'
    suggested_assessor = get_object_or_404(SuggestedAssessor, id=id)
    assessor = suggested_assessor.assessor
    if assessor.user != request.user:
        raise Http404

    qaa = suggested_assessor.qaa
    assessment_data, created = AssessmentData.objects.get_or_create(qaa=qaa)

    sd = SupportingDocuments.objects.all().filter(qaa=qaa)
    sd_1, created = sd.get_or_create(qaa=qaa, file_name='sd_1')
    sd_2, created = sd.get_or_create(qaa=qaa, file_name='sd_2')
    sd_3, created = sd.get_or_create(qaa=qaa, file_name='sd_3')
    sd_4, created = sd.get_or_create(qaa=qaa, file_name='sd_4')
    sd_5, created = sd.get_or_create(qaa=qaa, file_name='sd_5')
    sd_6, created = sd.get_or_create(qaa=qaa, file_name='sd_6')
    sd_7, created = sd.get_or_create(qaa=qaa, file_name='sd_7')
    sd_8, created = sd.get_or_create(qaa=qaa, file_name='sd_8')
    sd_9, created = sd.get_or_create(qaa=qaa, file_name='sd_9')
    context = {
        'suggested_assessor':suggested_assessor,
        'mode': mode,
        'assessor_view': True,
        'qaa': qaa,
        'sd_1':sd_1,
        'sd_2':sd_2,
        'sd_3':sd_3,
        'sd_4':sd_4,
        'sd_5':sd_5,
        'sd_6':sd_6,
        'sd_7':sd_7,
        'sd_8':sd_8,
        'sd_9':sd_9,
    }
    if request.method == 'POST':
        if 'reject' in request.POST:
            suggested_assessor.acception = 'reject'
            suggested_assessor.save()
            suggested_assessor.remarks = request.POST['remarks']
            messages.info(request,'Successfully reject the assessor assignation.')
        if 'accept' in request.POST:
            suggested_assessor.acception = 'accept'
            suggested_assessor.remarks = request.POST['remarks']
            suggested_assessor.save()

            AssignedAssessor.objects.get_or_create(
                ad=assessment_data,
                assessor=suggested_assessor.assessor,
                assessor_number=suggested_assessor.assessor_no,
                name=suggested_assessor.assessor.user.name,
                role_in_assessment='assessor',
            )

            # Check if suggested assessor is accepted
            all_suggested_assessor = SuggestedAssessor.objects.all().filter(qaa=qaa).exclude(assessor=None)
            complete = True
            for all in all_suggested_assessor:
                if all.acception != 'accept':
                    complete = False
                    break
            if complete == True:
                qaa.application_status = 'assessor_assign'
                qaa.save()

                # Assign Lead Assessor
                highest = -1
                lead_assessor = None
                for all in all_suggested_assessor:
                    temp = AssignedAssessor.objects.all().filter(assessor=all.assessor)
                    count = len(temp)
                    print('count:'+str(count))
                    if count > highest:
                        highest = count
                        lead_assessor = all.assessor
                lead_assigned_assessor = AssignedAssessor.objects.all().filter(assessor=lead_assessor,ad=assessment_data).first()
                lead_assigned_assessor.role_in_assessment = 'lead_assessor'
                lead_assigned_assessor.save()

            messages.info(request,'Successfully accept the assessor assignation.')
        return redirect('dashboard_application_assessor_list_own')    
    return render(request, "dashboard/application/application_info.html", context)

@login_required(login_url="/login/")
@allowed_users(allowed_roles=['superadmin','casc_verifier'])
def dashboard_application_assessor_change(request, id):
    current = get_object_or_404(SuggestedAssessor, id=id)
    assessors = Assessor.objects.all()
    if request.method == 'POST':
        assessor_id = request.POST['assessor_id']
        assessor = Assessor.objects.get(id=assessor_id)
        current.assessor = assessor
        current.assessor_no = assessor.assessor_no
        current.acception = None
        current.save()
        messages.info(request,'Successfully changed the Suggested Assessor')
        return redirect('dashboard_application_assessor_assign', current.qaa.id)
    context = {
        'current': current,
        'assessors': assessors
    }
    return render(request, "dashboard/application/assessor_change.html", context)


from decimal import Decimal

## Functions
def get_qaa_result(qaa):
    components = Component.objects.all().order_by('created_date')
    element_components = Element.objects.all().filter(category_weightage=True).order_by('created_date')
    sub_components = SubComponent.objects.all().filter().order_by('created_date')
    elements = Element.objects.all().filter(category_weightage=False).order_by('created_date')
    # defect_groups = DefectGroup.objects.all().order_by('-created_date')
    # sample_results = SampleResult.objects.all().filter(qaa=qaa)
    result = {}
    index_c = 'A'
    result['building_type'] = qaa.building_type
    result['components'] = []
    ## Component
    for component in components:
        index_sc = 1
        result_c = {}
        result_c['no'] = index_c
        result_c['name'] = component.name
        result_c['type'] = component.type
        if qaa.building_type == 'A':
            result_c['weightage'] = component.weightage_a
        if qaa.building_type == 'B':
            result_c['weightage'] = component.weightage_b
        if qaa.building_type == 'C':
            result_c['weightage'] = component.weightage_c
        if qaa.building_type == 'D':
            result_c['weightage'] = component.weightage_d
        result_c['subcomponents'] = []
        
        # To check if need to remove from weightage
        component_total_check = 0
        component_total_compliance = 0
        
        ## Sub Component
        for sub_component in sub_components:
            if sub_component.component == component:
                index_e = 1
                result_sc = {}
                result_sc['no'] = index_sc
                result_sc['name'] = sub_component.name
                result_sc['type'] = sub_component.type
                result_sc['weightage'] = sub_component.get_total_weightage()
                result_sc['elements'] = []
                
                ## Element
                for element in elements:
                    if element.sub_component == sub_component:
                        result_e = {}
                        result_e['no'] = str(index_sc) + "." + str(index_e)
                        result_e['name'] = element.name
                        result_e['weightage'] = element.weightage
                        
                        # Calculate Result
                        number_of_compliance = 0
                        number_of_check = 0
                        element_results = ElementResult.objects.all().filter(
                            Q(element_code=element.id)|
                            Q(element_code=element.code_id)
                        )
                        for element_result in element_results:
                            number_of_compliance += element_result.total_compliance
                            component_total_compliance += element_result.total_compliance

                            number_of_check += element_result.total_check
                            component_total_check += element_result.total_check

                        result_e['total_compliance'] = number_of_compliance
                        result_e['total_check'] = number_of_check

                        result_sc['elements'].append(result_e)
                        index_e += 1
                result_c['subcomponents'].append(result_sc)
                index_sc += 1
        

        result_c['total_compliance'] = component_total_compliance
        result_c['total_check'] = component_total_check
        result['components'].append(result_c)
        index_c = chr(ord(index_c) + 1)

    ## Element Component
    for element_component in element_components:
        index_sc = 1
        result_c = {}
        result_c['no'] = index_c
        result_c['name'] = element_component.name
        result_c['type'] = 3

        if qaa.building_type == 'A':
            result_c['weightage'] = element_component.weightage_a
        if qaa.building_type == 'B':
            result_c['weightage'] = element_component.weightage_b
        if qaa.building_type == 'C':
            result_c['weightage'] = element_component.weightage_c
        if qaa.building_type == 'D':
            result_c['weightage'] = element_component.weightage_d

        number_of_compliance = 0
        number_of_check = 0
        element_results = ElementResult.objects.all().filter(
            Q(element_code=element_component.id)|
            Q(element_code=element_component.code_id)
        )
        for element_result in element_results:
            number_of_compliance += element_result.total_compliance

            number_of_check += element_result.total_check


        result_c['total_compliance'] = number_of_compliance
        result_c['total_check'] = number_of_check
        result['components'].append(result_c)
        index_c = chr(ord(index_c) + 1)

    #### Calculate Result

    # Step 1. Recalculate Area Weightage
    total_area_weightage = 0
    for component in result['components']:
        if int(component['total_check']) > 0:
            total_area_weightage += Decimal(component['weightage'])
    for component in result['components']:
        if int(component['total_check']) > 0:
            component['actual_weightage'] = Decimal(component['weightage']) / total_area_weightage * 100
        else:
            component['actual_weightage'] = 0

    # Step 2. Recalculate Element Weightage
    for component in result['components']:
        if component['type'] == 1:
            total_element_weightage = 0
            if 'subcomponents' in component:
                for subcomponent in component['subcomponents']:
                    total_sub_component_weightage = 0
                    if 'elements' in subcomponent:
                        for element in subcomponent['elements']:
                            if int(element['total_check'] > 0):
                                total_element_weightage += Decimal(element['weightage'])
                                total_sub_component_weightage += Decimal(element['weightage'])
                    subcomponent['actual_weightage'] = total_sub_component_weightage
                
                # component['actual_weightage'] = total_element_weightage
                print(subcomponent['actual_weightage'])
                for subcomponent in component['subcomponents']:
                    if 'elements' in subcomponent:
                        for element in subcomponent['elements']:
                            if int(element['total_check']) > 0:
                                if Decimal(subcomponent['actual_weightage']) > 0:
                                    element['actual_weightage'] = element['weightage'] / Decimal(subcomponent['actual_weightage']) * 100
                                else:
                                    element['actual_weightage'] = 0
                            else:
                                element['actual_weightage'] = 0
    
    # Step 3: Calculate Score
    # for component in result['component']
    score = {}
    score['components'] = []
    for component in result['components']:
        score_c = {}
        score_c['no'] = component['no']
        score_c['name'] = component['name']
        score_c['total_weightage'] = component['actual_weightage']

        if component['type'] == 2 or component['type'] == 3:
            if component['total_check'] != 0:
                score_c['score'] = float(component['total_compliance']) / float(component['total_check']) * float(component['actual_weightage'])
            else:
                score_c['score'] = 0
            score['components'].append(score_c)
        if component['type'] == 1:
            total_score_sub_component = 0
            score_sc_array = []
            if 'subcomponents' in component:
                    for subcomponent in component['subcomponents']:
                        score_sc = {}
                        score_sc['no'] = subcomponent['no']
                        score_sc['name'] = subcomponent['name']
                        score_sc['total_weightage'] = subcomponent['actual_weightage']
                        if subcomponent['type'] == 0:
                            total_score_element = 0
                            if 'elements' in subcomponent:
                                for element in subcomponent['elements']:
                                    if element['total_check'] != 0:
                                        element_score = float(element['total_compliance']) / float(element['total_check']) * float(element['actual_weightage'])
                                        total_score_element += element_score
                            score_sc['score'] = 0
                        score_sc_array.append(score_sc)
                        if subcomponent['type'] == 3 or subcomponent['type'] == 2:
                            if 'elements' in subcomponent:
                                for element in subcomponent['elements']:
                                    score_sc = {}
                                    score_sc['no'] = element['no']
                                    score_sc['name'] = element['name']
                                    score_sc['total_weightage'] = element['actual_weightage']

                                    if element['total_check'] != 0:
                                        element_score = float(element['total_compliance']) / float(element['total_check']) * float(element['actual_weightage'])
                                        score_sc['score'] = element_score
                                        total_score_sub_component += element_score
                                    else:
                                        score_sc['score'] = 0
                                    score_sc_array.append(score_sc)
            print(total_score_sub_component)
            score_c['score'] = total_score_sub_component * float(component['actual_weightage']) / 100
            score['components'].append(score_c)
            for arr in score_sc_array:
                score['components'].append(arr)

    # print(result)
    return score

## AJAX
@login_required(login_url="/login/")
def ajax_api_application_payment_request(request):
    print('aasds')
    if request.method == 'POST':
        id = request.POST['id']
        qaa = get_object_or_404(QlassicAssessmentApplication, id=id)
        response = create_transaction(request, qaa.no_of_blocks, 'QLC', 'PERMOHONAN PENILAIAN QLASSIC', qaa.qaa_number, request.user)
        print(response)
        proforma = response.Code
        result = response.TransactionResult
        
        response_url = get_domain(request) + '/dashboard/application/payment/'+id+'/response/'

        # Create Payment
        payment, created = Payment.objects.get_or_create(order_id=proforma)
        payment.user = request.user
        payment.customer_name = request.user.name
        payment.customer_email = request.user.email
        payment.qaa = qaa
        payment.currency = 'MYR'
        payment.payment_amount = response.Amount
        payment.save()

        postdata = {
            'payment_gateway_url':payment_gateway_url,
            'ClientReturnURL':response_url,
            'IcOrRoc':request.user.code_id,
            'OrderID':proforma,
            'Currency':"MYR",
            'TransactionType':"SALE",
            'ClientRef0':"",
            'ClientRef1':"",
            'ClientRef2':"",
            'ClientRef3':"",
            'ClientRef4':"",
            'Amount': payment.payment_amount,
            'CustomerName':request.user.name,
            'CustomerEmail':request.user.email,
            'CustomerPhoneNo':request.user.hp_no,
            'result':result,
        }

        return JsonResponse(postdata)
    else:
        return JsonResponse({})
