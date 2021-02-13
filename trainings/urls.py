# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.urls import path, re_path
from . import views

urlpatterns = [

    ### Training Module
    path('dashboard/training/application/new/', views.dashboard_training_application_new, name="dashboard_training_application_new"),
    path('dashboard/training/list/', views.dashboard_training_list, name="dashboard_training_list"),
    path('dashboard/training/new/', views.dashboard_training_new, name="dashboard_training_new"),
    path('dashboard/training/feedback/trainee/', views.dashboard_training_feedback_list_trainee, name="dashboard_training_feedback_list_trainee"),
    path('dashboard/training/feedback/staff/', views.dashboard_training_feedback_list_staff, name="dashboard_training_feedback_list_staff"),
    path('dashboard/training/feedback/application/<str:id>/', views.dashboard_training_feedback_application, name="dashboard_training_feedback_application"),
    path('dashboard/training/feedback/review/<str:id>/', views.dashboard_training_feedback_review, name="dashboard_training_feedback_review"),
    path('dashboard/training/application/dashboard/', views.dashboard_training_application_dashboard, name="dashboard_training_application_dashboard"),
    path('dashboard/training/application/list/', views.dashboard_training_role_application_list, name="dashboard_training_role_application_list"),
    path('dashboard/training/application/new/<str:application_type>/<str:step>/', views.dashboard_training_application_new, name="dashboard_training_application_new"),
    path('dashboard/training/application/review/<str:id>/<str:step>/', views.dashboard_training_role_application_review, name="dashboard_training_role_application_review"),
    path('dashboard/training/joined/certificate/', views.dashboard_joined_training_certificate, name="dashboard_joined_training_certificate"),
    path('dashboard/training/joined/list/', views.dashboard_joined_training_list, name="dashboard_joined_training_list"),
    path('dashboard/training/joined/payment/<str:id>/', views.dashboard_joined_training_pay, name="dashboard_joined_training_pay"),
    path('dashboard/training/joined/payment/<str:id>/response/', views.dashboard_joined_training_pay_response, name="dashboard_joined_training_pay_response"),
    path('dashboard/training/available/', views.dashboard_available_training_list, name="dashboard_available_training_list"),
    path('dashboard/training/join/<str:id>/', views.dashboard_training_join, name="dashboard_training_join"),
    path('dashboard/training/participant/<str:id>/', views.dashboard_training_participant, name="dashboard_training_participant"),
    path('dashboard/training/participant/review/<str:id>/', views.dashboard_training_participant_review, name="dashboard_training_participant_review"),
    path('dashboard/training/id/<str:id>/', views.dashboard_training_update, name="dashboard_training_update"),
    path('dashboard/training/coach/<str:id>/', views.dashboard_training_coach_update, name="dashboard_training_coach_update"),
    path('dashboard/training/review/<str:id>/', views.dashboard_training_review, name="dashboard_training_review"),
    path('dashboard/training/attendance/<str:id>/', views.dashboard_training_attendance_trainer, name="dashboard_training_attendance_trainer"),
    path('dashboard/training/attendance/<str:id>/review/', views.dashboard_training_attendance_review, name="dashboard_training_attendance_review"),
]
