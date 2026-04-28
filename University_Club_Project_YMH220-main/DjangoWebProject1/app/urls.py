# -*- coding: utf-8 -*-
from django.urls import path
from . import views

urlpatterns = [
    # Home
    path('', views.home, name='home'),

    # Authentication
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('register/', views.register_view, name='register'),

    # Student Dashboard
    path('dashboard/', views.dashboard, name='dashboard'),
    path('profile/edit/', views.profile_edit, name='profile_edit'),

    # Club Admin Panel
    path('club-admin/', views.club_admin, name='club_admin'),

    # System Admin Panel
    path('system-admin/', views.system_admin, name='system_admin'),

    # Clubs
    path('clubs/', views.club_list, name='club_list'),
    path('clubs/<int:pk>/', views.club_detail, name='club_detail'),
    path('clubs/add/', views.club_add, name='club_add'),
    path('clubs/<int:pk>/edit/', views.club_edit, name='club_edit'),
    path('clubs/<int:pk>/delete/', views.club_delete, name='club_delete'),
    path('clubs/<int:pk>/approve/', views.club_approve, name='club_approve'),
    path('clubs/<int:pk>/info/', views.club_info, name='club_info'),

    # Events
    path('events/', views.event_list, name='event_list'),
    path('events/add/', views.event_add, name='event_add'),
    path('events/<int:pk>/', views.event_detail, name='event_detail'),
    path('events/<int:pk>/edit/', views.event_edit, name='event_edit'),
    path('events/<int:pk>/delete/', views.event_delete, name='event_delete'),
    path('events/<int:pk>/approve/', views.event_approve, name='event_approve'),
    path('events/<int:pk>/register/', views.event_register, name='event_register'),
    path('events/archive/', views.event_archive, name='event_archive'),

    # Registrations
    path('registrations/<int:pk>/approve/', views.registration_approve, name='registration_approve'),
    path('registrations/<int:pk>/reject/', views.registration_reject, name='registration_reject'),

    # Students
    path('students/', views.student_list, name='student_list'),
    path('students/add/', views.student_add, name='student_add'),
    path('students/<int:pk>/edit/', views.student_edit, name='student_edit'),
    path('students/<int:pk>/delete/', views.student_delete, name='student_delete'),

    # Membership Requests
    path('membership/', views.membership_requests_view, name='membership_requests'),
    path('membership/apply/<int:club_id>/', views.membership_apply, name='membership_apply'),
    path('membership/<int:pk>/approve/', views.membership_approve, name='membership_approve'),
    path('membership/<int:pk>/reject/', views.membership_reject, name='membership_reject'),

    # Announcements
    path('announcements/', views.announcements, name='announcements'),
    path('announcements/add/', views.announcement_add, name='announcement_add'),
    path('announcements/<int:pk>/', views.announcement_detail, name='announcement_detail'),
    path('announcements/<int:pk>/edit/', views.announcement_edit, name='announcement_edit'),
    path('announcements/<int:pk>/delete/', views.announcement_delete, name='announcement_delete'),

    # Messages
    path('messages/', views.messages_view, name='messages'),

    # Core Team
    path('clubs/<int:pk>/core-team/apply/', views.core_team_apply, name='core_team_apply'),
    path('core-team/<int:pk>/approve/', views.core_team_approve, name='core_team_approve'),
    path('core-team/<int:pk>/reject/', views.core_team_reject, name='core_team_reject'),
    path('membership/<int:pk>/remove/', views.member_remove, name='member_remove'),
]
