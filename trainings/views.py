from datetime import datetime
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.db.models import Q
from django.views.decorators.csrf import csrf_exempt

# Decorators
from django.contrib.auth.decorators import login_required
from authentication.decorators import allowed_users

# Models
from .models import (
    RoleApplication,
    Coach,
    Training,
    RegistrationTraining,
    JoinedTraining,
    ORGANIZATION_TYPE_CHOICES,
    Feedback,
)

from users.models import (
    CustomUser, Trainer,
    Assessor,
    AcademicQualification, 
    WorkExperience,
)

from billings.models import Payment

# Forms
from .forms import (
    AttendanceSheetUploadForm,
    CoachCreateForm,
    TrainingCreateForm,
    RegistrationTrainingCreateForm,
    RegistrationTrainingReviewForm,
    FeedbackCreateForm,
)

# Helpers
from .helpers import (
    check_available_seat,
    get_trainer_application_status,
    get_assessor_application_status,
    get_trainer_application,
    get_assessor_application,
    get_role_application_supporting_documents,
    save_role_application_supporting_documents,
    # generate_role_application_number,
)
from billings.helpers import payment_response_process

from core.helpers import translate_malay_date, standard_date, send_email_default, send_email_with_attachment
from app.helpers.letter_templates import generate_document, generate_document_file, generate_training_document_file
from api.soap.create_transaction import create_transaction, payment_gateway_url

# Create your views here.
@login_required(login_url="/login/")
@allowed_users(allowed_roles=['superadmin', 'trainer', 'assessor', 'trainee', 'applicant'])
def dashboard_training_application_dashboard(request):
    if request.user.role != 'assessor' and request.user.role != 'trainer' and request.user.role != 'superadmin':
        messages.warning(request, 'You must be either QLASSIC Industry Assessor (QIA), QLASSIC CIDB Assessor (QCA) or Trainer in order to apply the role(s) below.')
    # application, applicable = get_trainer_application(request, request.user, 'trainer')
    application_trainer, applicable_trainer = get_trainer_application_status(request.user)
    application_assessor, applicable_assessor = get_assessor_application_status(request.user)
    assessor = Assessor.objects.all().filter(user=request.user)
    trainer = Trainer.objects.all().filter(user=request.user)
    context = {
        'assessor':assessor,
        'trainer':trainer,
        'application_trainer':application_trainer,
        'applicable_trainer':applicable_trainer,
        'application_assessor':application_assessor,
        'applicable_assessor':applicable_assessor,
    }
    return render(request, "dashboard/training/role_application_dashboard.html", context)

@login_required(login_url="/login/")
@allowed_users(allowed_roles=['superadmin', 'cidb_reviewer'])
def dashboard_training_role_application_list(request):
    applications = RoleApplication.objects.all().exclude(application_status='').order_by('-modified_date')
    context = {
        'applications':applications,
    }
    return render(request, "dashboard/training/role_application_list.html", context)

# @allowed_users(allowed_roles=['superadmin', 'trainer'])
# @login_required(login_url="/login/")
# def dashboard_training_application_new(request):
#     context = {
#         'mode': 'step_1',
#     }
#     # if request.method == 'POST':
#     #     application_type = 
#     #     application, applicable = get_trainer_application(request, request.user, 'trainer')
#     return render(request, "dashboard/training/application_form.html", context)

@login_required(login_url="/login/")
@allowed_users(allowed_roles=['superadmin', 'trainer','assessor'])
def dashboard_training_application_new(request, application_type, step):
    context = {
        'application_type': application_type,
        'mode': step,
    }

    applicable = False
    application = None
    if application_type == 'qca':
        application, applicable = get_assessor_application(request, request.user)
        context['application'] = application
    if application_type == 'trainer':
        application, applicable = get_trainer_application(request, request.user)
        context['application'] = application
    if applicable:
        pass
    else:
        messages.warning(request, 'Unable to apply the role.')
        return redirect('dashboard_training_application_dashboard')
    
    if step == 'step-2':
        academic_qualifications = AcademicQualification.objects.all().filter(user=request.user)
        context['academic_qualifications'] = academic_qualifications
    
    if step == 'step-3':
        work_experiences = WorkExperience.objects.all().filter(user=request.user)
        context['work_experiences'] = work_experiences
    
    if step == 'step-4':
        registration_trainings = RegistrationTraining.objects.all().filter(user=request.user, status='accepted', attendance_full=True)
        joined_trainings = JoinedTraining.objects.all().filter(user=request.user)
        context['registration_trainings'] = registration_trainings
        context['joined_trainings'] = joined_trainings
        if request.method == 'POST':
            if 'add' in request.POST:
                jt_year = request.POST['year']
                jt_course = request.POST['course']
                jt_place = request.POST['place']
                jt = JoinedTraining.objects.create(user=request.user, year=jt_year, course=jt_course, place=jt_place)
                messages.info(request, 'Added the joined training info.')
            if 'delete' in request.POST:
                jt_id = request.POST['id']
                jt = JoinedTraining.objects.get(id=jt_id)
                jt.delete()
                messages.info(request, 'Deleted the joined training.')
            return redirect('dashboard_training_application_new', application_type, step)

    if step == 'step-5':
        work_experiences = WorkExperience.objects.all().filter(user=request.user)
        context['supporting_documents'] = get_role_application_supporting_documents(application)
        if request.method == 'POST':
            save_role_application_supporting_documents(request, application)
            if 'save' in request.POST:
                return redirect('dashboard_training_application_new', application_type, step)

            if 'submit' in request.POST:
                application.application_status = 'pending'
                # generate_role_application_number(application)
                application.save()

                 # Email
                to = []
                reviewers = CustomUser.objects.all().filter(
                    Q(role='superadmin')|
                    Q(role='cidb_reviewer')
                )
                for reviewer in reviewers:
                    to.append(reviewer.email)
                subject = "Role Application Submission - " + application.application_number
                ctx_email = {
                    'application':application,
                }
                messages.info(request, 'Successfully send the role application.')
                send_email_default(subject, to, ctx_email, 'email/role-application-submission.html')

                return redirect('dashboard_training_application_dashboard')

    return render(request, "dashboard/training/role_application_form.html", context)

@login_required(login_url="/login/")
@allowed_users(allowed_roles=['superadmin', 'cidb_reviewer'])
def dashboard_training_role_application_review(request, id, step):
    application = get_object_or_404(RoleApplication, id=id)
    context = {
        'review': True,
        'id': id,
        'application': application,
        'mode': step,
    }

    if step == 'step-2':
        academic_qualifications = AcademicQualification.objects.all().filter(user=request.user)
        context['academic_qualifications'] = academic_qualifications
    
    if step == 'step-3':
        work_experiences = WorkExperience.objects.all().filter(user=request.user)
        context['work_experiences'] = work_experiences
    
    if step == 'step-4':
        registration_trainings = RegistrationTraining.objects.all().filter(user=request.user, status='accepted', attendance_full=True)
        joined_trainings = JoinedTraining.objects.all().filter(user=request.user)
        context['registration_trainings'] = registration_trainings
        context['joined_trainings'] = joined_trainings
        # if request.method == 'POST':
        #     if 'add' in request.POST:
        #         jt_year = request.POST['year']
        #         jt_course = request.POST['course']
        #         jt_place = request.POST['place']
        #         jt = JoinedTraining.objects.create(user=request.user, year=jt_year, course=jt_course, place=jt_place)
        #         messages.info(request, 'Added the joined training info.')
        #     if 'delete' in request.POST:
        #         jt_id = request.POST['id']
        #         jt = JoinedTraining.objects.get(id=jt_id)
        #         jt.delete()
        #         messages.info(request, 'Deleted the joined training.')
        #     return redirect('dashboard_training_application_new', application_type, step)

    if step == 'step-5':
        work_experiences = WorkExperience.objects.all().filter(user=request.user)
        context['supporting_documents'] = get_role_application_supporting_documents(application)
        # if request.method == 'POST':
        #     save_role_application_supporting_documents(request, application)
        #     if 'save' in request.POST:
        #         return redirect('dashboard_training_application_new', application_type, step)
        #     if 'submit' in request.POST:
        #         application.application_status = 'pending'
        #         # generate_role_application_number(application)
        #         application.save()
        #         return redirect('dashboard_training_application_dashboard')

    if request.method == "POST":
        if 'interview' in request.POST:
            # Save Data
            date = request.POST['date']
            time_from = request.POST['time_from']
            time_to = request.POST['time_to']
            location = request.POST['location']
            application.interview_date = date
            application.interview_time_from = time_from
            application.interview_time_to = time_to
            application.interview_location = location
            application.application_status = 'interview_invitation'
            application.reviewed_by = request.user.name
            application.save()

            # Create Letter Template

            # Interview Letter
            template_ctx = {
                'name': application.user.name,
                'ic': application.user.icno,
                'company': application.user.organization,
                'date': translate_malay_date(standard_date(datetime.now())),
            }
            if application.application_type == 'trainer':
                response = generate_document_file(request, 'interview_trainer', template_ctx)
                application.interview_letter_file.save('pdf', response)
            if application.application_type == 'qca':
                response = generate_document_file(request, 'interview_qca', template_ctx)
                application.interview_letter_file.save('pdf', response)

            # Email
            to = ['muhaafidz@gmail.com']
            subject = "Interview Invitation"
            attachments = [application.interview_letter_file.path]
            messages.info(request, 'Successfully delivered an email to trainer(s).')
            send_email_with_attachment(subject, to, {}, 'email/interview-trainer-invitation.html', attachments)
      
            
        if 'reject' in request.POST:
            pass
        if 'accreditation' in request.POST:
            pass

    return render(request, "dashboard/training/role_application_form.html", context)

@login_required(login_url="/login/")
@allowed_users(allowed_roles=['superadmin', 'trainer', 'cidb_reviewer'])
def dashboard_training_list(request):
    mode = 'list'
    trainings = Training.objects.all()
    if request.user.role != 'superadmin' and request.user.role != 'cidb_reviewer':
        trainings = trainings.filter(trainer=request.user)

    context = {
        'title': 'Manage Training',
        'mode': mode,
        'trainings': trainings,
    }
    return render(request, "dashboard/training/manage_training.html", context)

@login_required(login_url="/login/")
@allowed_users(allowed_roles=['superadmin', 'trainer'])
def dashboard_training_new(request):
    mode = 'create'
    training_form = TrainingCreateForm()
    context = {
        'title': 'Add New Training',
        'mode': mode,
        'training_form': training_form,
    }
    if request.method == 'POST':
        training_form = TrainingCreateForm(request.POST)
        if training_form.is_valid():
            training = training_form.save()
            training.trainer = request.user
            training.created_by = request.user.name
            training.save()
            messages.info(request, 'Created successfully')
            return redirect('dashboard_training_update', training.id)
        else:
            messages.warning(request, 'Unable to create new training')
    return render(request, "dashboard/training/manage_training.html", context)


@login_required(login_url="/login/")
@allowed_users(allowed_roles=['superadmin', 'trainer'])
def dashboard_training_update(request, id):
    mode = 'update'
    training = get_object_or_404(Training, id=id)
    training_form = TrainingCreateForm(instance=training)
    coaches = Coach.objects.all().filter(training=training)
    coach_form = CoachCreateForm()
    context = {
        'title': 'Update Training',
        'mode': mode,
        'training_form': training_form,
        'coach_form': coach_form,
        'training': training,
        'coaches':coaches,
    }

    if request.method == 'POST':
        if 'update_training' in request.POST:
            training_form = TrainingCreateForm(request.POST, instance=training)
            if training_form.is_valid():
                form = training_form.save()
                form.modified_by = request.user.name
                form.save()
                messages.info(request, 'Updated successfully')
            else:
                messages.warning(request, 'Unable to update training')
        if 'create_coach' in request.POST:
            coach_form = CoachCreateForm(request.POST)
            if coach_form.is_valid():
                form = coach_form.save()
                form.training = training
                form.created_by = request.user.name
                form.save()
                messages.info(request, 'Added successfully')
            else:
                messages.warning(request, 'Unable to add new coach:'+coach_form.errors.as_text())
        return redirect('dashboard_training_update', training.id)
    return render(request, "dashboard/training/manage_training.html", context)

@login_required(login_url="/login/")
@allowed_users(allowed_roles=['superadmin', 'cidb_reviewer'])
def dashboard_training_review(request, id):
    mode = 'review'
    training = get_object_or_404(Training, id=id)
    training_form = TrainingCreateForm(instance=training)
    coaches = Coach.objects.all().filter(training=training)
    coach_form = CoachCreateForm()
    context = {
        'title': 'Review Training',
        'mode': mode,
        'training_form': training_form,
        'coach_form': coach_form,
        'training': training,
        'coaches': coaches,
    }

    if request.method == 'POST':
        if 'reject' in request.POST:
            training.review_status = 'rejected'
            training.save()
            messages.info(request, 'Rejected successfully')
        if 'accept' in request.POST:
            training.review_status = 'accepted'
            training.save()
            messages.info(request, 'Accept successfully')
        return redirect('dashboard_training_list')
    return render(request, "dashboard/training/manage_training.html", context)

@login_required(login_url="/login/")
@allowed_users(allowed_roles=['superadmin', 'trainer'])
def dashboard_training_coach_update(request, id):
    coach = get_object_or_404(Coach, id=id)
    training = coach.training
    coach_form = CoachCreateForm(instance=coach)
    context = {
        'title': 'Manage Coach',
        'training': training,
        'coach_form': coach_form,
    }

    if request.method == 'POST':
        if 'update' in request.POST:
            coach_form = CoachCreateForm(request.POST, instance=coach)
            if coach_form.is_valid():
                form = coach_form.save()
                form.modified_by = request.user.name
                form.save()
                messages.info(request, 'Updated successfully')
            else:
                messages.warning(request, 'Unable to update coach information')
        if 'delete' in request.POST:
            training_id = coach.training.id
            coach.delete()
            messages.info(request, 'Delete successfully')
            return redirect('dashboard_training_update', training_id)
        return redirect('dashboard_training_coach_update', coach.id)
    return render(request, "dashboard/training/coach_form.html", context)

@login_required(login_url="/login/")
@allowed_users(allowed_roles=['superadmin', 'trainer', 'cidb_reviewer', 'applicant', 'trainee'])
def dashboard_available_training_list(request):
    mode = 'all'
    trainings = Training.objects.all().filter(review_status='accepted')
    context = {
        'title': 'Available Training List',
        'mode': mode,
        'trainings': trainings,
    }
    return render(request, "dashboard/training/enroll_training.html", context)

@login_required(login_url="/login/")
@allowed_users(allowed_roles=['superadmin', 'trainer', 'applicant', 'trainee'])
def dashboard_joined_training_list(request):
    mode = 'joined_training'
    trainings = RegistrationTraining.objects.all().filter(user=request.user)
    context = {
        'title': 'Joined Training',
        'mode': mode,
        'trainings': trainings,
    }
    return render(request, "dashboard/training/enroll_training.html", context)

@login_required(login_url="/login/")
@allowed_users(allowed_roles=['superadmin', 'applicant', 'trainee'])
def dashboard_joined_training_pay(request, id):
    mode = 'payment'
    rt = get_object_or_404(RegistrationTraining, id=id)
    response = create_transaction(request, rt.training.fee, 0, 'QLC-PUP', rt.code_id, request.user)
    proforma = response.Code
    
    # Create Payment
    payment, created = Payment.objects.get_or_create(order_id=proforma)
    payment.user = request.user
    payment.customer_name = request.user.name
    payment.customer_email = request.user.email
    payment.rt = rt
    payment.currency = 'MYR'
    payment.payment_amount = rt.training.fee
    payment.save()

    context = {
        'title': 'Payment - Joined Training',
        'mode': mode,
        'training': rt,
        'proforma': proforma,
        'response': response,
        'url': payment_gateway_url,
    }
    return render(request, "dashboard/training/enroll_training.html", context)

@csrf_exempt
def dashboard_joined_training_pay_response(request, id):
    mode = 'payment_response'
    payment = None
    rt = get_object_or_404(RegistrationTraining, id=id)
    if request.method == 'POST':
        payment = payment_response_process(request)
        if payment.payment_status == 1:
            rt.status = 'accepted'
            rt.save()
    context = {
        'title': 'Payment Response - Joined Training',
        'mode': mode,
        'training': rt,
        'payment': payment,
    }
    return render(request, "dashboard/training/enroll_training.html", context)

@login_required(login_url="/login/")
@allowed_users(allowed_roles=['superadmin', 'cidb_reviewer', 'trainer', 'applicant', 'trainee'])
def dashboard_training_participant(request, id):
    mode = 'participant'
    training = get_object_or_404(Training, id=id)
    available_seat, is_available = check_available_seat(request, training)
    participants = RegistrationTraining.objects.all().filter(training__id = id)
    context = {
        'title': 'List of Participant',
        'mode': mode,
        'participants': participants,
        'training': training,
        'available_seat': available_seat,
        'is_available': is_available,
    }
    return render(request, "dashboard/training/enroll_training.html", context)

@login_required(login_url="/login/")
@allowed_users(allowed_roles=['superadmin', 'cidb_reviewer'])
def dashboard_training_participant_review(request, id):
    mode = 'participant_review'
    rt = get_object_or_404(RegistrationTraining, id=id)
    training = rt.training
    form_review = RegistrationTrainingReviewForm()
    available_seat, is_available = check_available_seat(request, training)
    context = {
        'title': 'Participant Review',
        'mode': mode,
        'rt': rt,
        'training': training,
        'available_seat': available_seat,
        'is_available': is_available,
        'form_review': form_review,
    }
    if request.method == 'POST':
        if 'accept' in request.POST:
            form_review = RegistrationTrainingReviewForm(request.POST, instance=rt)
            if form_review.is_valid():
                form = form_review.save()
                form.reviewed_by = request.user.name
                form.status = 'need_payment'
                form.save()
                messages.info(request, 'Accepted the participant successfully')

                # Email
                to = []
                to.append(rt.user.email)
                subject = "Request to Join Training - " + rt.code_id + " (" + training.training_name + ")"
                ctx_email = {
                    'training':training,
                    'rt': rt,
                }
                send_email_default(subject, to, ctx_email, 'email/training-join-response.html')

            else:
                messages.warning(request, 'Unable to review the participant')
        if 'reject' in request.POST:
            form_review = RegistrationTrainingReviewForm(request.POST, instance=rt)
            if form_review.is_valid():
                form = form_review.save()
                form.reviewed_by = request.user.name
                form.status = 'rejected'
                form.save()
                messages.info(request, 'Rejected the participant successfully')

                  # Email
                to = []
                to.append(rt.user.email)
                subject = "Request to Join Training - " + rt.code_id + " (" + training.training_name + ")"
                ctx_email = {
                    'training':training,
                    'user': rt.user,
                }
                send_email_default(subject, to, ctx_email, 'email/training-join-response.html')
            else:
                messages.warning(request, 'Unable to review the participant')
        return redirect('dashboard_training_participant', training.id)
    return render(request, "dashboard/training/enroll_training.html", context)

@login_required(login_url="/login/")
@allowed_users(allowed_roles=['superadmin', 'trainee', 'applicant'])
def dashboard_training_join(request, id):
    training = get_object_or_404(Training, id=id)
    existing = RegistrationTraining.objects.all().filter(training=training, user=request.user).order_by('-created_date')
    if len(existing) > 0:
        current = existing[0]
        if current.status == 'pending':
            messages.warning(request, 'Unable to register the training. You already applied this training. Please wait for the approval.')
            return redirect('dashboard_available_training_list')
        elif current.status == 'accepted':
            messages.warning(request, 'Unable to register the training. You have been accepted to join this training.')
            return redirect('dashboard_available_training_list')
        elif current.status == 'need_payment':
            messages.warning(request, 'Unable to register the training. You already applied this training. Please proceed with the payment.')
            return redirect('dashboard_available_training_list')
        else:
            pass

    available_seat, is_available = check_available_seat(request, training)
    mode = 'register'
    print(type(ORGANIZATION_TYPE_CHOICES))
    context = {
        'title': 'Join Training',
        'mode': mode,
        'organization_type_choices': ORGANIZATION_TYPE_CHOICES,
        'training': training,
        'available_seat': available_seat,
        'is_available': is_available,
    }

    if request.method == 'POST':
        rt = RegistrationTraining.objects.create(training=training, user=request.user)
        rt.participant_name = request.user.name
        rt.participant_icno = request.user.icno
        rt.participant_email = request.user.email
        rt.participant_hpno = request.user.hp_no
        rt.participant_organization = request.user.organization
        rt.participant_organization_type = request.POST['participant_organization_type']
        rt.participant_designation = request.POST['participant_designation']
        rt.save()

        # Email
        cidb_reviewers = CustomUser.objects.all().filter(
            Q(role='cidb_reviewer')|
            Q(role='superadmin')
        )
        to = []
        for reviewer in cidb_reviewers:
            to.append(reviewer.email)
        subject = "Request to Join Training - " + rt.code_id + " (" + training.training_name + ")"
        ctx_email = {
            'training':training,
        }
        send_email_default(subject, to, ctx_email, 'email/training-join-request.html')

        messages.warning(request, 'Successfully request to join the training. Please wait for approval from reviewer before proceeding with payment.')
        return redirect('dashboard_joined_training_list')

    return render(request, "dashboard/training/enroll_training.html", context)

@login_required(login_url="/login/")
@allowed_users(allowed_roles=['superadmin', 'trainer'])
def dashboard_training_attendance_trainer(request, id):
    training = get_object_or_404(Training, id=id)
    attendances = RegistrationTraining.objects.all().filter(training=training, status='accepted')
    attendance_sheet_form = AttendanceSheetUploadForm(instance=training)
    mode = 'trainer'
    context = {
        'attendance_sheet_form': attendance_sheet_form,
        'title': 'Mark Attendance List - ' + training.training_name,
        'mode': mode,
        'training': training,
        'attendances': attendances,
    }
    if request.method == 'POST':
        if 'upload_attendance_sheet' in request.POST:
            attendance_sheet_form = AttendanceSheetUploadForm(request.POST, request.FILES, instance=training)
            attendance_sheet_form.save()
            messages.info(request, 'Successfully upload the attendance sheet.')
        elif 'approval' in request.POST:
            if training.attendance_sheet_file != '':
                training.attendance_review_status = 'need_approval'
                training.save()
                messages.info(request, 'Successfully send the attendance for approval.')
            else:
                messages.warning(request, 'You must upload the attendance sheet file before sending the attendance for approval.')
        elif 'generate_template' in request.POST:
            trainers = Coach.objects.all().filter(training=training)
            venue = training.address1 + ', ' + training.address2 + ', ' + training.postcode + ' ' + training.city + ', ' + training.state
            tmpl_ctx = {
                'training_name': training.training_name,
                'trainers': trainers,
                'venue': venue,
                'days': range(training.number_of_days()),
                'from_date': translate_malay_date(standard_date(training.from_date)),
                'to_date': translate_malay_date(standard_date(training.to_date)),
                'from_time': training.from_time,
                'to_time': training.to_time,
                'participants': attendances,
            }
            response = generate_document(request, 'attendance_sheet', tmpl_ctx)
            return response 
        else:
            participant_id = request.POST['id']
            rt = RegistrationTraining.objects.get(id=participant_id)
            if 'attend_full' in request.POST:
                rt.attendance_full = True
                rt.save()
                messages.info(request, 'Changed attendance as FULL')
            if 'attend_not_full' in request.POST:
                rt.attendance_full = False
                rt.save()
                messages.info(request, 'Changed attendance as NOT FULL')
            if 'mark' in request.POST:
                rt.marks = request.POST['marks']
                rt.save()
                messages.info(request, 'Changed marks')
        return redirect('dashboard_training_attendance_trainer', training.id)

    return render(request, "dashboard/training/attendance.html", context)

@login_required(login_url="/login/")
@allowed_users(allowed_roles=['superadmin', 'cidb_reviewer'])
def dashboard_training_attendance_review(request, id):
    training = get_object_or_404(Training, id=id)
    attendances = RegistrationTraining.objects.all().filter(training=training, status='accepted')
    mode = 'reviewer'
    context = {
        'title': 'Review Attendance List - ' + training.training_name,
        'mode': mode,
        'training': training,
        'attendances': attendances,
    }

    if request.method == 'POST':
        if 'generate' in request.POST:
            for attendance in attendances:
                if attendance.attendance_full == True:
                    if training.cert_type == 'pass':
                        if attendance.marks >= training.passing_mark:
                            attendance.pass_status = True
                        else:
                            attendance.pass_status = False
                    else:
                        attendance.pass_status = True
                else:
                    attendance.pass_status = False
                
                generate_pdf = False

                if attendance.pass_status == True:
                    generate_pdf = True
                else:
                    if training.cert_type == 'pass':
                        generate_pdf = True
                    
                if generate_pdf == True:   
                    template_ctx = {
                        'name': attendance.user.name,
                        'ic': attendance.user.icno,
                        'company': attendance.user.organization,
                        'date': translate_malay_date(standard_date(datetime.now())),
                    }
                    response = generate_training_document_file(request, training.training_type, template_ctx)
                    attendance.certificate_file.save('pdf', response)

                attendance.save()
            messages.info(request, 'Successfully generated the document for participants.')  
        if 'approve' in request.POST:
            training.attendance_review_status = 'approved'
            training.save()
            messages.info(request, 'Successfully approved the attendance.')  
        return redirect('dashboard_training_attendance_review', training.id)

    return render(request, "dashboard/training/attendance.html", context)

@login_required(login_url="/login/")
@allowed_users(allowed_roles=['trainee', 'applicant'])
def dashboard_training_feedback_list_trainee(request):
    feedbacks = Feedback.objects.all().filter(user=request.user)

    context = {
        'role': 'trainee',
        'feedbacks':feedbacks,
    }

    return render(request, "dashboard/training/feedback_list.html", context)

@login_required(login_url="/login/")
@allowed_users(allowed_roles=['superadmin', 'cidb_reviewer'])
def dashboard_training_feedback_list_staff(request):
    feedbacks = Feedback.objects.all()

    context = {
        'role': 'staff',
        'feedbacks':feedbacks,
    }

    return render(request, "dashboard/training/feedback_list.html", context)

@login_required(login_url="/login/")
@allowed_users(allowed_roles=['trainee', 'applicant'])
def dashboard_training_feedback_application(request, id):
    training = get_object_or_404(Training, id=id)
    context = {
        'training':training,
    }

    if request.method == 'POST':
        form = FeedbackCreateForm(request.POST)
        if form.is_valid():
            data = form.save()
            data.user = request.user
            data.training = training
            data.save()
            messages.info(request, 'Successfully send the feedback.')
            return redirect('dashboard_joined_training_list')
        else:
            messages.warning(request, 'Problem with sending the feedback.')
            return redirect('dashboard_training_feedback_application', training.id)

    return render(request, "dashboard/training/feedback_application.html", context)

@login_required(login_url="/login/")
@allowed_users(allowed_roles=['superadmin', 'cidb_reviewer'])
def dashboard_training_feedback_review(request, id):
    feedback = get_object_or_404(Feedback, id=id)
    trainers = Coach.objects.all().filter(training=feedback.training)
    print(len(trainers))
    mode = 'review'
    context = {
        'mode': mode,
        'feedback':feedback,
        'trainers':trainers,
    }

    if request.method == 'POST':
        feedback.warning = request.POST['warning']
        feedback.warning_delivered = True
        feedback.warning_delivered_date = datetime.now()
        feedback.reviewer = request.user
        feedback.save()

        # Email
        to = []
        for trainer in trainers:
            to.append(trainer.email)
        subject = "Complaint From Trainee - " + feedback.training.training_name
        ctx_email = {
            'feedback':feedback,
        }
        messages.info(request, 'Successfully delivered an email to trainer(s).')
        send_email_default(subject, to, ctx_email, 'email/training-complaint.html')
           
        return redirect('dashboard_training_feedback_review', feedback.id)

    return render(request, "dashboard/training/feedback_application.html", context)

@login_required(login_url="/login/")
@allowed_users(allowed_roles=['superadmin', 'cidb_reviewer', 'trainee', 'applicant', 'trainer', 'assessor'])
def dashboard_joined_training_certificate(request):
    trainings = RegistrationTraining.objects.all().filter(user=request.user, pass_status=True)

    context = {
        'role': 'staff',
        'trainings':trainings,
    }

    return render(request, "dashboard/training/certificate_list.html", context)
