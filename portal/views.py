# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages

# Forms
from users.forms import UserUpdateForm, WorkExperienceCreateForm, AcademicQualificationCreateForm
from portal.forms import AnnouncementCreateForm, PublicationCreateForm, TrainingCreateForm

# Models
from users.models import WorkExperience, AcademicQualification
from portal.models import Announcement, Publication, Training

# Decorators
from authentication.decorators import allowed_users

### Admin - Portal Module ###
@login_required(login_url="/login/")
def dashboard(request):
    return redirect('dashboard_profile')

@login_required(login_url="/login/")
def dashboard_profile(request):
    user = request.user
    academic_qualifications = AcademicQualification.objects.all().filter(user=request.user)
    work_experiences = WorkExperience.objects.all().filter(user=request.user)
    
    form_user = UserUpdateForm(instance=user)
    form_we = WorkExperienceCreateForm()
    form_aq = AcademicQualificationCreateForm()

    if request.method == 'POST':
        if 'update' in request.POST:
            form_user = UserUpdateForm(request.POST, request.FILES or None, instance=user)
            if form_user.is_valid():
                form_user.save()
                messages.info(request, 'Updated successfully')
            else:
                messages.warning(request, 'Unable to update profile: ' + form_user.errors.as_text())
        if 'create_we' in request.POST:
            form_we = WorkExperienceCreateForm(request.POST)
            if form_we.is_valid():
                we = form_we.save()
                we.user = request.user
                we.save()
                messages.info(request, 'Created successfully')
            else:
                messages.warning(request, 'Unable to create work experience: ' + form_we.errors.as_text())
        if 'create_aq' in request.POST:
            form_aq = AcademicQualificationCreateForm(request.POST)
            if form_aq.is_valid():
                aq = form_aq.save()
                aq.user = request.user
                aq.save()
                messages.info(request, 'Created successfully')
            else:
                messages.warning(request, 'Unable to create academic qualification: ' + form_aq.errors.as_text())
        return redirect('dashboard_profile')
    
    if request.user.icno == None or request.user.icno == '':
        messages.warning(request,'Please update your profile to complete the registration.')
        
    context = { 'form_user': form_user,'form_we':form_we,'form_aq':form_aq,'work_experiences':work_experiences,'academic_qualifications':academic_qualifications}
    return render(request, "dashboard/portal/profile.html", context)

@login_required(login_url="/login/")
def dashboard_profile_work_experience(request, id):
    user = request.user
    we = get_object_or_404(WorkExperience, user=user, id=id)
    mode = 'we'
    form = WorkExperienceCreateForm(instance=we)
    context = {
        'we': we,
        'form': form,
        'mode': mode,
    }
    if request.method == 'POST':
        if 'delete' in request.POST:
            we.delete()
            messages.info(request, 'Delete successfully')
            return redirect('dashboard_profile')
        if 'update' in request.POST:
            form = WorkExperienceCreateForm(request.POST, instance=we)
            if form.is_valid():
                form.save()
                messages.info(request, 'Successfully updating the work experience')
            else:
                messages.warning(request, 'Error updating the work experience')
            return redirect('dashboard_profile_work_experience', id)
                
    return render(request, "dashboard/portal/profile_detail.html", context)

@login_required(login_url="/login/")
def dashboard_profile_academic_qualification(request, id):
    user = request.user
    aq = get_object_or_404(AcademicQualification, user=user, id=id)
    mode = 'aq'
    form = AcademicQualificationCreateForm(instance=aq)
    context = {
        'aq': aq,
        'form': form,
        'mode': mode,
    }
    if request.method == 'POST':
        if 'delete' in request.POST:
            aq.delete()
            messages.info(request, 'Delete successfully')
            return redirect('dashboard_profile')
        if 'update' in request.POST:
            form = AcademicQualificationCreateForm(request.POST, instance=aq)
            if form.is_valid():
                form.save()
                messages.info(request, 'Successfully updating the academic qualification')
            else:
                messages.warning(request, 'Error updating the academic qualification')
            return redirect('dashboard_profile_academic_qualification', id)
                
    return render(request, "dashboard/portal/profile_detail.html", context)

@login_required(login_url="/login/")
@allowed_users(allowed_roles=['superadmin'])
def dashboard_announcement(request):
    announcements = Announcement.objects.all()
    form_announcement = AnnouncementCreateForm()
    if request.method == 'POST':
        if 'create' in request.POST:
            form_announcement = AnnouncementCreateForm(request.POST)
            if form_announcement.is_valid():
                ann = form_announcement.save()
                ann.created_by = request.user.name
                ann.save()
                messages.info(request, 'Created successfully')
            else:
                messages.warning(request, 'Unable to create new announcement')

        return redirect('dashboard_announcement')
    context = {"announcements": announcements, 'form_announcement':form_announcement}
    return render(request, "dashboard/portal/announcement.html", context)

@login_required(login_url="/login/")
@allowed_users(allowed_roles=['superadmin'])
def dashboard_announcement_id(request, id):
    announcement = get_object_or_404(Announcement, id=id)
    form_announcement = AnnouncementCreateForm(instance=announcement)
    if request.method == 'POST':
        if 'delete' in request.POST:
            announcement.delete()
            messages.info(request, 'Deleted successfully')
            return redirect('dashboard_announcement')
        if 'update' in request.POST:
            form_announcement = AnnouncementCreateForm(request.POST,instance=announcement)
            if form_announcement.is_valid():
                ann = form_announcement.save()
                ann.modified_by = request.user.name
                ann.save()
                messages.info(request, 'Updated successfully')
            else:
                messages.warning(request, 'Unable to update announcement')

        return redirect('dashboard_announcement_id', id)
    context = {"announcement": announcement,'form_announcement': form_announcement}
    return render(request, "dashboard/portal/announcement_id.html", context)

@login_required(login_url="/login/")
@allowed_users(allowed_roles=['superadmin'])
def dashboard_publication(request):
    publications = Publication.objects.all()
    form_publication = PublicationCreateForm()
    if request.method == 'POST':
        if 'create' in request.POST:
            form_publication = PublicationCreateForm(request.POST, request.FILES or None)
            if form_publication.is_valid():
                pub = form_publication.save()
                pub.modified_by = request.user.name
                pub.save()
                messages.info(request, 'Created successfully')
            else:
                messages.warning(request, 'Unable to create new publication')
        return redirect('dashboard_publication')
    context = {"publications": publications, 'form_publication': form_publication}
    return render(request, "dashboard/portal/publication.html", context)

@login_required(login_url="/login/")
@allowed_users(allowed_roles=['superadmin'])
def dashboard_publication_id(request, id):
    publication = get_object_or_404(Publication, id=id)
    form_publication = PublicationCreateForm(instance=publication)
    if request.method == 'POST':
        if 'delete' in request.POST:
            publication.delete()
            messages.info(request, 'Deleted successfully')
            return redirect('dashboard_publication')
        if 'update' in request.POST:
            form_publication = PublicationCreateForm(request.POST,instance=publication)
            if form_publication.is_valid():
                pub = form_publication.save()
                pub.modified_by = request.user.name
                pub.save()
                messages.info(request, 'Updated successfully')
            else:
                messages.warning(request, 'Unable to update publication')

        return redirect('dashboard_publication_id', id)
    context = {"publication": publication,'form_publication': form_publication}
    return render(request, "dashboard/portal/publication_id.html", context)

@login_required(login_url="/login/")
@allowed_users(allowed_roles=['superadmin'])
def dashboard_training(request):
    trainings = Training.objects.all()
    form_training = TrainingCreateForm()
    if request.method == 'POST':
        if 'create' in request.POST:
            form_training = TrainingCreateForm(request.POST, request.FILES or None)
            if form_training.is_valid():
                tra = form_training.save()
                tra.modified_by = request.user.name
                tra.save()
                messages.info(request, 'Created successfully')
            else:
                messages.warning(request, 'Unable to create new training')
        return redirect('dashboard_training')
    context = {"trainings": trainings, 'form_training': form_training}
    return render(request, "dashboard/portal/training.html", context)

@login_required(login_url="/login/")
@allowed_users(allowed_roles=['superadmin'])
def dashboard_training_id(request, id):
    training = get_object_or_404(Training, id=id)
    form_training = TrainingCreateForm(instance=training)
    if request.method == 'POST':
        if 'delete' in request.POST:
            training.delete()
            messages.info(request, 'Deleted successfully')
            return redirect('dashboard_training')
        if 'update' in request.POST:
            form_training = TrainingCreateForm(request.POST, request.FILES or None ,instance=training)
            if form_training.is_valid():
                tra = form_training.save()
                tra.modified_by = request.user.name
                tra.save()
                messages.info(request, 'Updated successfully')
            else:
                messages.warning(request, 'Unable to update training')
        return redirect('dashboard_training_id', id)
    context = {"training": training,'form_training':form_training}
    return render(request, "dashboard/portal/training_id.html", context)