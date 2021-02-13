# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.http import Http404
import datetime
import random

# Forms
from users.forms import UserUpdateForm
from assessments.forms import QAACreateForm, QAAApplicationForm, QAAReviewForm, QAAVerifyForm, SupportingDocumentsUploadForm
from projects.forms import ProjectInfoCreateForm, ProjectInfoApplicationForm

# Models
from users.models import Assessor
from projects.models import Contractor, ProjectInfo
from assessments.models import QlassicAssessmentApplication, SupportingDocuments, SuggestedAssessor, AssignedAssessor, AssessmentData

# Decorators
from authentication.decorators import allowed_users

### Admin - Application Module ###
@login_required(login_url="/login/")
def dashboard_application_overview(request):
    return render(request, "dashboard/application/overview.html")

@allowed_users(allowed_roles=['superadmin'])
@login_required(login_url="/login/")
def dashboard_application(request):
    return render(request, "dashboard/application/list.html")

@allowed_users(allowed_roles=['contractor'])
@login_required(login_url="/login/")
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

@login_required(login_url="/login/")
def dashboard_application_project(request):
    contractors = Contractor.objects.all().filter(qaa_number=None)
    context = {
        'contractors':contractors,
    }
    return render(request, "dashboard/application/project_list.html", context)

@allowed_users(allowed_roles=['superadmin','contractor','applicant'])
@login_required(login_url="/login/")
def dashboard_application_new(request, id):
    contractor = get_object_or_404(Contractor, id=id)
    qaa = None
    qaa_created = False

    qaa_all = QlassicAssessmentApplication.objects.all().filter(contractor=contractor).order_by('-created_date')
    if qaa_all.count() > 0:
        qaa_latest = qaa_all[0]
        print(qaa_latest.id)
        if qaa_latest.application_status == 'rejected':
            qaa = QlassicAssessmentApplication.objects.create(contractor=contractor)
            qaa_created = True
        elif qaa_latest.application_status == 'rejected_amendment':
            qaa = qaa_latest
        elif qaa_latest.application_status == None or qaa_latest.application_status == '':
            qaa = qaa_latest
        else:
            raise Http404      
    else:
        qaa = QlassicAssessmentApplication.objects.create(contractor=contractor)
        qaa_created = True

    if qaa_created:
        qaa.user = request.user
    
    # Refresh new information  
    qaa.contractor = contractor
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
    qaa.contract_type = contractor.contract_type
    if contractor.project_type == 'GOVERNMENT':
        qaa.payment_mode = 'off'
    else:
        qaa.payment_mode = 'on'
    qaa.save()
        
    form_qaa = QAACreateForm(instance=qaa)
    if request.method == 'POST':
        form_qaa = QAAApplicationForm(request.POST,instance=qaa)
        if form_qaa.is_valid():
            qaa = form_qaa.save()
            messages.info(request,'Successfully save')

            return redirect('dashboard_application_new_2', contractor.id)
        else:
            messages.warning(request,'Problem with details'+form_qaa.errors.as_text())
            return redirect('dashboard_application_new', contractor.id)

    #     if contractor.qaa_number == None:
            
            
    #         qaa = QlassicAssessmentApplication.objects.get_or_create(
    #             first_name='John',
    #             last_name='Lennon',
    #             defaults={'birthday': date(1940, 10, 9)},
    #         )
    context = {'qaa':qaa, 'form_qaa':form_qaa, 'contractor':contractor}
    return render(request, "dashboard/application/application_form_1.html",context)

@login_required(login_url="/login/")
def dashboard_application_new_2(request, id):
    contractor = get_object_or_404(Contractor, id=id)
    
    qaa = QlassicAssessmentApplication.objects.all().filter(contractor=contractor).order_by('-created_date')[0]

    pi, pi_created = ProjectInfo.objects.get_or_create(qaa=qaa)
    
    if pi_created:
        pi.qaa = qaa

    # Refresh new information  
    pi.project_type = contractor.project_type
    pi.levy_number = contractor.levy_number
    pi.project_title = contractor.project_title
    pi.contractor_name = contractor.name_of_contractor
    pi.contractor_cidb_registration_no = contractor.contractor_registration_number
    pi.contractor_cidb_registration_grade = contractor.contractor_registration_grade
    pi.contract_value = contractor.contract_value
    pi.project_location = contractor.project_location
    pi.save()

    form_pi = ProjectInfoCreateForm(instance=pi)
    if request.method == 'POST':
        form_pi = ProjectInfoApplicationForm(request.POST, instance=pi)
        if form_pi.is_valid():
            qaa = form_pi.save()
            messages.info(request,'Successfully save')

            return redirect('dashboard_application_new_3', contractor.id)
        else:
            messages.warning(request,'Problem with details'+form_pi.errors.as_text())
            return redirect('dashboard_application_new_2', contractor.id)

    context = {'pi':pi,'form_pi':form_pi, 'contractor':contractor}
    return render(request, "dashboard/application/application_form_2.html",context)


@login_required(login_url="/login/")
def dashboard_application_new_3(request, id):
    contractor = get_object_or_404(Contractor, id=id)
    
    qaa = QlassicAssessmentApplication.objects.all().filter(contractor=contractor).order_by('-created_date')[0]

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
            sd_1.file = form_sd.cleaned_data.get('sd_1')
            sd_2.file = form_sd.cleaned_data.get('sd_2')
            sd_3.file = form_sd.cleaned_data.get('sd_3')
            sd_4.file = form_sd.cleaned_data.get('sd_4')
            sd_5.file = form_sd.cleaned_data.get('sd_5')
            sd_6.file = form_sd.cleaned_data.get('sd_6')
            sd_7.file = form_sd.cleaned_data.get('sd_7')
            sd_8.file = form_sd.cleaned_data.get('sd_8')
            sd_9.file = form_sd.cleaned_data.get('sd_9')
            sd_1.save()
            sd_2.save()
            sd_3.save()
            sd_4.save()
            sd_5.save()
            sd_6.save()
            sd_7.save()
            sd_8.save()
            sd_9.save()
            
            # Change status to pending
            qaa.application_status = 'pending'
            
            # Generate QAA Number
            qaa_count = ProjectInfo.objects.filter(project_location=contractor.project_location,qaa__building_type=qaa.building_type,project_type=contractor.project_type).exclude(qaa__qaa_number='').count()
            qaa_number = ''
            new_number = False
            while new_number==False:
                qaa_count += 1
                qaa_number = contractor.project_location + datetime.datetime.now().strftime('%y') + qaa.building_type + str(qaa_count).zfill(5) + " Q (" + contractor.project_type + ")"
                check_qaa_exist = QlassicAssessmentApplication.objects.all().filter(qaa_number=qaa_number)
                if check_qaa_exist.count() == 0:
                    new_number=True

            qaa.qaa_number = qaa_number
            qaa.date_created = datetime.datetime.now()
            qaa.save()

            contractor.qaa_number = qaa.qaa_number
            contractor.save()

            messages.info(request,'QLASSIC Assessment Application completed')

            return redirect('dashboard_application_list')
        else:
            messages.warning(request, 'Problem with uploading the documents: '+form_sd.errors.as_text())
        return redirect('dashboard_application_new_3', contractor.id)

    return render(request, "dashboard/application/application_form_3.html",context)

@login_required(login_url="/login/")
def dashboard_application_review(request, id):
    mode = 'review'

    pi = get_object_or_404(ProjectInfo, qaa__id=id)
    qaa = pi.qaa
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
        'pi':pi,
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
        if 'reject' in request.POST:
            contractor = Contractor.objects.get(qaa_number=qaa.qaa_number)
            contractor.qaa_number = None
            contractor.save()
            qaa.remarks1 = request.POST['remarks1']
            qaa.application_status = 'rejected'
            qaa.save()
            messages.info(request,'Successfully rejected the application')
            return redirect('dashboard_application_list')
        if 'reject_amendment' in request.POST:
            qaa.application_status = 'rejected_amendment'
            qaa.remarks1 = request.POST['remarks1']
            qaa.verified_by = request.user.name
            qaa.verified_date = datetime.datetime.now()
            qaa.save()
            messages.info(request,'Successfully rejected (with amendment) the application')
            return redirect('dashboard_application_list')
        if 'accept' in request.POST:
            form_review = QAAReviewForm(request.POST, instance=qaa)
            if form_review.is_valid():
                review = form_review.save()
                review.reviewed_by = request.user.name
                review.reviewed_date = datetime.datetime.now()
                review.application_status = 'reviewed'
                review.save()
                messages.info(request,'Successfully reviewed the application')
                return redirect('dashboard_application_list')
            else:
                messages.warning(request,'Problem with reviewing the application:'+form_review.errors.as_text())
                return redirect('dashboard_application_review', qaa.id)
        
    return render(request, "dashboard/application/application_info.html", context)

@login_required(login_url="/login/")
def dashboard_application_verify(request, id):
    mode = 'verify'

    pi = get_object_or_404(ProjectInfo, qaa__id=id)
    qaa = pi.qaa

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
        'pi':pi,
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
        if 'reject' in request.POST:
            contractor = Contractor.objects.get(qaa_number=qaa.qaa_number)
            contractor.qaa_number = None
            contractor.save()
            qaa.remarks2 = request.POST['remarks2']
            qaa.application_status = 'rejected'
            qaa.save()
            messages.info(request,'Successfully rejected the application')
            return redirect('dashboard_application_list')
        if 'reject_amendment' in request.POST:
            qaa.application_status = 'rejected_amendment'
            qaa.remarks2 = request.POST['remarks2']
            qaa.verified_by = request.user.name
            qaa.verified_date = datetime.datetime.now()
            qaa.save()
            messages.info(request,'Successfully rejected (with amendment) the application')
            return redirect('dashboard_application_list')
        if 'accept' in request.POST:
            form_verify = QAAVerifyForm(request.POST, instance=qaa)
            if form_verify.is_valid():
                verify = form_verify.save()
                verify.verified_by = request.user.name
                verify.verified_date = datetime.datetime.now()
                if verify.payment_mode == 'off':
                    verify.application_status = 'verified'
                else:
                    verify.application_status = 'need_payment'
                verify.save()

                # Remove current suggestion
                assessors = SuggestedAssessor.objects.all().filter(qaa=verify)
                assessors.delete()

                # Create suggested assessor based on value set by verifier and assign the assessor randomly
                sas = SuggestedAssessor.objects.all().filter(qaa=verify)
                i = 0
                ass_list = list(Assessor.objects.all())
                random.shuffle(ass_list)
                for x in range(verify.no_of_assessor):
                    sa = SuggestedAssessor.objects.create(qaa=verify)
                    if i < len(ass_list):
                        print(ass_list[i])
                        sa.assessor = ass_list[i]
                        sa.assessor_no = ass_list[i].assessor_no
                        sa.save()
                    i = i + 1

                messages.info(request,'Successfully verified the application')
                return redirect('dashboard_application_list')
            else:
                messages.warning(request,'Problem with verifying the application:'+form_review.errors.as_text())
                return redirect('dashboard_application_verify', qaa.id)
    return render(request, "dashboard/application/application_info.html", context)

@login_required(login_url="/login/")
def dashboard_application_list(request):
    pis = ProjectInfo.objects.all()
    user_pis = ProjectInfo.objects.all().filter(qaa__user=request.user)
    context = {
        'pis':pis,
        'user_pis':user_pis,    
    }
    if request.method == 'POST':
        if 'reapply' in request.POST:
            id = request.POST['id']
            contractor = Contractor.objects.get(id=id)
            return redirect('dashboard_application_new', contractor.id)
    return render(request, "dashboard/application/application_list.html",context)

@login_required(login_url="/login/")
def dashboard_application_payment(request):
    pis = ProjectInfo.objects.all().filter(qaa__application_status='need_payment',qaa__user=request.user)
    context = { 'pis':pis }
    return render(request, "dashboard/application/payment.html",context)

@login_required(login_url="/login/")
def dashboard_application_assessor_list(request):
    pis = ProjectInfo.objects.all().filter(qaa__application_status='verified')
    context = { 'pis':pis }
    return render(request, "dashboard/application/assessor_list.html", context)

@login_required(login_url="/login/")
def dashboard_application_assessor_assign(request, id):
    mode = 'assign_assessor'
    
    pi = get_object_or_404(ProjectInfo, qaa__id=id)
    qaa = pi.qaa
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
        'pi':pi,
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
        assessment_data = AssessmentData.get_or_create(qaa=qaa)
        for sa in suggested_assessors:
            aa = AssignedAssessor.objects.create(
                    ad=assessment_data,
                    assessor=sa.assessor,

                )
    return render(request, "dashboard/application/application_info.html", context)

@allowed_users(allowed_roles=['superadmin','casc_verifier'])
@login_required(login_url="/login/")
def dashboard_application_assessor_approve(request, id):
    pi = get_object_or_404(ProjectInfo, qaa__id=id)
    mode = 'verify_assessor'
    context = { 
        'mode':mode, 
        'pi':pi 
    }
    return render(request, "dashboard/application/application_info.html", context)

@allowed_users(allowed_roles=['superadmin','casc_verifier'])
@login_required(login_url="/login/")
def dashboard_application_assessor_change(request, id):
    current = get_object_or_404(SuggestedAssessor, id=id)
    assessors = Assessor.objects.all()
    if request.method == 'POST':
        assessor_id = request.POST['assessor_id']
        assessor = Assessor.objects.get(id=assessor_id)
        current.assessor = assessor
        current.assessor_no = assessor.assessor_no
        current.save()
        messages.info(request,'Successfully changed the Suggested Assessor')
        return redirect('dashboard_application_assessor_assign', current.qaa.id)
    context = {
        'current': current,
        'assessors': assessors
    }
    return render(request, "dashboard/application/assessor_change.html", context)

### Claim Module ###
@login_required(login_url="/login/")
def dashboard_claim_assessor_info(request):
    return render(request, "dashboard/claim/profile.html")

@login_required(login_url="/login/")
def dashboard_claim_list_mileage(request):
    mode = 'mileage'
    context = {
        'mode': mode,
    }
    return render(request, "dashboard/claim/list.html", context)

@login_required(login_url="/login/")
def dashboard_claim_list_fi(request):
    mode = 'fi'
    context = {
        'mode': mode,
    }
    return render(request, "dashboard/claim/list.html", context)

@login_required(login_url="/login/")
def dashboard_claim_list_transport(request):
    mode = 'transport'
    context = {
        'mode': mode,
    }
    return render(request, "dashboard/claim/list.html", context)

@login_required(login_url="/login/")
def dashboard_claim_list_accommodation(request):
    mode = 'accommodation'
    context = {
        'mode': mode,
    }
    return render(request, "dashboard/claim/list.html", context)

@login_required(login_url="/login/")
def dashboard_claim_list_other(request):
    mode = 'other'
    context = {
        'mode': mode,
    }
    return render(request, "dashboard/claim/list.html", context)