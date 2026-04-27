"""
Definition of views.
"""

from django.shortcuts import render

def home(request):
    return render(request, 'app/index.html')

def dashboard(request):
    return render(request, 'app/dashboard.html')

def club_admin(request):
    # Bu sadece kulüp baþkanýnýn (Örn: BT Kulübü) kendi panelidir
    return render(request, 'app/club_admin.html')

def system_admin(request):
    # Bu dökümandaki en son attýðýnýz "Sistem Yöneticisi" panelidir
    return render(request, 'app/system_admin.html')

def event_detail(request):
    return render(request, 'app/event_detail.html')

# YENÝ EKLENEN: Puanlama ve Arþiv Sayfasý
def event_archive(request):
    return render(request, 'app/event_archive.html')

def announcements(request):
    return render(request, 'app/announcements.html')

def messages(request):
    return render(request, 'app/messages.html')


from datetime import datetime
from django.shortcuts import render
from django.http import HttpRequest

def home(request):
    """Renders the home page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/index.html',
        {
            'title':'Home Page',
            'year':datetime.now().year,
        }
    )

def contact(request):
    """Renders the contact page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/contact.html',
        {
            'title':'Contact',
            'message':'Your contact page.',
            'year':datetime.now().year,
        }
    )

def about(request):
    """Renders the about page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/about.html',
        {
            'title':'About',
            'message':'Your application description page.',
            'year':datetime.now().year,
        }
    )
