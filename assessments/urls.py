# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.urls import path, re_path
from . import views

urlpatterns = [

    ### Application Module
    path('dashboard/application/overview/', views.dashboard_application_overview, name="dashboard_application_overview"),
    path('dashboard/application/', views.dashboard_application, name="dashboard_application"),
    path('dashboard/application/new/<str:contractor_registration_number>/<str:id>/', views.dashboard_application_new, name="dashboard_application_new"),
    path('dashboard/application/new/<str:contractor_registration_number>/<str:id>/2/', views.dashboard_application_new_2, name="dashboard_application_new_2"),
    path('dashboard/application/new/<str:contractor_registration_number>/<str:id>/3/', views.dashboard_application_new_3, name="dashboard_application_new_3"),
    path('dashboard/application/list/', views.dashboard_application_list, name="dashboard_application_list"),
    path('dashboard/application/profile/', views.dashboard_application_profile, name="dashboard_application_profile"),
    path('dashboard/application/project/', views.dashboard_application_project, name="dashboard_application_project"),
    path('dashboard/application/info/<str:id>/', views.dashboard_application_info, name="dashboard_application_info"),
    path('dashboard/application/info/<str:id>/<str:assessor_mode>/assessment/', views.dashboard_application_info_assessor, name="dashboard_application_info_assessor"),
    path('dashboard/application/review/<str:id>/', views.dashboard_application_review, name="dashboard_application_review"),
    path('dashboard/application/verify/<str:id>/', views.dashboard_application_verify, name="dashboard_application_verify"),
    path('dashboard/application/payment/<str:id>/', views.dashboard_application_payment, name="dashboard_application_payment"),
    path('dashboard/application/payment/<str:id>/response/', views.dashboard_application_payment_response, name="dashboard_application_payment_response"),
    # path('dashboard/application/assessor/list/', views.dashboard_application_assessor_list, name="dashboard_application_assessor_list"),
    path('dashboard/application/assessor/list/all/', views.dashboard_application_assessor_list_all, name="dashboard_application_assessor_list_all"),
    path('dashboard/application/assessor/list/', views.dashboard_application_assessor_list_own, name="dashboard_application_assessor_list_own"),
    path('dashboard/application/assessor/assign/<str:id>/', views.dashboard_application_assessor_assign, name="dashboard_application_assessor_assign"),
    path('dashboard/application/assessor/verify/<str:id>/', views.dashboard_application_assessor_approve, name="dashboard_application_assessor_approve"),

    ### Assign Assessor
    path('dashboard/application/assessor/<str:id>/change/', views.dashboard_application_assessor_change, name="dashboard_application_assessor_change"),
]
