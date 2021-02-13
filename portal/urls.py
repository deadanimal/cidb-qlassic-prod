# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.urls import path, re_path
from . import views

urlpatterns = [
    # Admin Profile
    path('dashboard/', views.dashboard, name="dashboard"),
    path('dashboard/profile/', views.dashboard_profile, name="dashboard_profile"),
    path('dashboard/profile/work-experience/<str:id>', views.dashboard_profile_work_experience, name="dashboard_profile_work_experience"),
    path('dashboard/profile/academic-qualification/<str:id>', views.dashboard_profile_academic_qualification, name="dashboard_profile_academic_qualification"),
    
    # Admin Portal
    path('dashboard/announcement/', views.dashboard_announcement, name="dashboard_announcement"),
    path('dashboard/announcement/<str:id>/', views.dashboard_announcement_id, name="dashboard_announcement_id"),
    path('dashboard/publication/', views.dashboard_publication, name="dashboard_publication"),
    path('dashboard/publication/<str:id>', views.dashboard_publication_id, name="dashboard_publication_id"),
    path('dashboard/training/', views.dashboard_training, name="dashboard_training"),
    path('dashboard/training/<str:id>', views.dashboard_training_id, name="dashboard_training_id"),
    #path('dashboard/user/', views.dashboard_user, name="dashboard_user"),

]
