from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('kulup-yonetimi/', views.club_admin, name='club_admin'),
    path('etkinlik-detay/', views.event_detail, name='event_detail'),
    path('etkinlik-arsivi/', views.event_archive, name='event_archive'),
    # YENÝ EKLENEN:
    path('duyurular/', views.announcements, name='announcements'),
    path('mesajlar/', views.messages, name='messages'),
    path('sistem-admin/', views.system_admin, name='system_admin'),
]