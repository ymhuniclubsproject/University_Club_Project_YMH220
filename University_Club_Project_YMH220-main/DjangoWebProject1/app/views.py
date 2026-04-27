# -*- coding: utf-8 -*-
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages as django_messages
from django.utils import timezone
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import (
    Club, Student, Event, MembershipRequest,
    EventRegistration, EventRating, Announcement, Message, CoreTeamApplication
)
from .forms import (
    ClubForm, StudentForm, EventForm, MembershipRequestForm,
    EventRegistrationForm, EventRatingForm, AnnouncementForm, MessageForm,
    UserRegistrationForm, LoginForm, CoreTeamApplicationForm
)


# ─────────────────────────────────────
# AUTHENTICATION
# ─────────────────────────────────────
def register_view(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            # Create student profile automatically if it doesn't exist
            Student.objects.get_or_create(
                student_id=str(user.id),
                defaults={
                    'full_name': user.username,
                    'department': "General",
                    'email': user.email or f"{user.username}@university.edu"
                }
            )
            django_messages.success(request, "Registration successful. You can now log in.")
            return redirect('login')
    else:
        form = UserRegistrationForm()
    return render(request, 'app/register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                django_messages.success(request, f"Welcome, {username}!")
                return redirect('home')
            else:
                django_messages.error(request, "Invalid username or password.")
    else:
        form = LoginForm()
    return render(request, 'app/login.html', {'form': form})

def logout_view(request):
    logout(request)
    django_messages.success(request, "You have been logged out.")
    return redirect('home')


# ─────────────────────────────────────
# HOME
# ─────────────────────────────────────
def home(request):
    # Show all active and approved events (or just upcoming ones)
    events = Event.objects.filter(is_approved=True).order_by('event_date')[:6]
    clubs = Club.objects.filter(is_active=True, is_approved=True)[:6]
    return render(request, 'app/index.html', {'events': events, 'clubs': clubs})


# ─────────────────────────────────────
# STUDENT DASHBOARD
# ─────────────────────────────────────
@login_required
def dashboard(request):
    students = Student.objects.all()
    events = Event.objects.filter(is_approved=True, status='upcoming')
    registrations = EventRegistration.objects.all()
    return render(request, 'app/dashboard.html', {
        'students': students,
        'events': events,
        'registrations': registrations,
    })


# ─────────────────────────────────────
# CLUB ADMIN PANEL
# ─────────────────────────────────────
@login_required
def club_admin(request):
    if request.user.username != 'UNICLUBSADMIN':
        django_messages.error(request, "Only the System Admin can access this panel.")
        return redirect('home')
    clubs = Club.objects.all()
    events = Event.objects.all()
    membership_requests = MembershipRequest.objects.filter(status='pending')
    core_team_apps = CoreTeamApplication.objects.filter(status='pending')
    return render(request, 'app/club_admin.html', {
        'clubs': clubs,
        'events': events,
        'membership_requests': membership_requests,
        'core_team_apps': core_team_apps,
        'total_members': Student.objects.count(),
        'active_events': Event.objects.filter(status='upcoming').count(),
        'pending_requests': membership_requests.count() + core_team_apps.count(),
    })


# ─────────────────────────────────────
# SYSTEM ADMIN PANEL
# ─────────────────────────────────────
@login_required
def system_admin(request):
    if request.user.username != 'UNICLUBSADMIN':
        django_messages.error(request, "Only the System Admin can access this panel.")
        return redirect('home')
    pending_clubs = Club.objects.filter(is_approved=False)
    pending_events = Event.objects.filter(is_approved=False)
    all_clubs = Club.objects.all()
    all_students = Student.objects.all()
    recent_registrations = EventRegistration.objects.order_by('-registered_at')[:10]
    return render(request, 'app/system_admin.html', {
        'pending_clubs': pending_clubs,
        'pending_events': pending_events,
        'all_clubs': all_clubs,
        'all_students': all_students,
        'recent_registrations': recent_registrations,
        'total_members': Student.objects.count(),
        'total_clubs': Club.objects.count(),
        'total_events': Event.objects.count(),
    })


# ─────────────────────────────────────
# CLUBS CRUD
# ─────────────────────────────────────
def club_list(request):
    clubs = Club.objects.filter(is_active=True)
    return render(request, 'app/club_list.html', {'clubs': clubs})


def club_detail(request, pk):
    club = get_object_or_404(Club, pk=pk)
    
    # Get all events for this club
    events = club.events.filter(is_approved=True)
    
    # Member count (Approved requests)
    members = Student.objects.filter(membership_requests__club=club, membership_requests__status='approved')
    
    # Calculate Club Rating (Average of its events)
    all_ratings = EventRating.objects.filter(event__club=club)
    avg_rating = None
    if all_ratings.exists():
        avg_rating = round(sum(r.score for r in all_ratings) / all_ratings.count(), 1)
    
    return render(request, 'app/club_detail.html', {
        'club': club,
        'events': events,
        'members': members,
        'avg_rating': avg_rating,
    })


def club_add(request):
    if not request.user.is_authenticated or request.user.username != 'UNICLUBSADMIN':
        django_messages.error(request, "Only Admin can add clubs.")
        return redirect('home')
    if request.method == 'POST':
        form = ClubForm(request.POST, request.FILES)
        if form.is_valid():
            club = form.save(commit=False)
            club.is_approved = True
            club.save()
            
            # Auto-create announcement if recruiting
            if club.is_recruiting:
                Announcement.objects.create(
                    title=f"New Recruitment: {club.name}",
                    content=f"{club.name} is now looking for new members! Apply now on their club page.",
                    announcement_type='club',
                    club=club
                )
            
            django_messages.success(request, 'Club added successfully!')
            return redirect('home')
    else:
        form = ClubForm()
    return render(request, 'app/club_form.html', {'form': form, 'title': 'Add New Club'})


def club_edit(request, pk):
    if not request.user.is_authenticated or request.user.username != 'UNICLUBSADMIN':
        django_messages.error(request, "Only Admin can edit clubs.")
        return redirect('home')
    club = get_object_or_404(Club, pk=pk)
    if request.method == 'POST':
        form = ClubForm(request.POST, request.FILES, instance=club)
        if form.is_valid():
            was_recruiting = club.is_recruiting
            club = form.save()
            
            # Auto-create announcement if just started recruiting
            if club.is_recruiting and not was_recruiting:
                Announcement.objects.create(
                    title=f"Recruitment Drive: {club.name}",
                    content=f"{club.name} has started accepting new members! Visit their page to join.",
                    announcement_type='club',
                    club=club
                )
            
            django_messages.success(request, 'Club updated successfully!')
            return redirect('club_admin')
    else:
        form = ClubForm(instance=club)
    return render(request, 'app/club_form.html', {'form': form, 'title': 'Edit Club', 'club': club})


def club_delete(request, pk):
    if not request.user.is_authenticated or request.user.username != 'UNICLUBSADMIN':
        django_messages.error(request, "Only Admin can delete clubs.")
        return redirect('home')
    club = get_object_or_404(Club, pk=pk)
    if request.method == 'POST':
        club.delete()
        django_messages.success(request, 'Club deleted.')
        return redirect('club_admin')
    return render(request, 'app/confirm_delete.html', {'object': club, 'type': 'Club', 'cancel_url': 'club_admin'})


def club_approve(request, pk):
    club = get_object_or_404(Club, pk=pk)
    club.is_approved = True
    club.save()
    django_messages.success(request, f'"{club.name}" has been approved.')
    return redirect('system_admin')


# ─────────────────────────────────────
# EVENTS CRUD
# ─────────────────────────────────────
def event_list(request):
    events = Event.objects.filter(is_approved=True)
    return render(request, 'app/event_archive.html', {'events': events})


def event_add(request):
    if not request.user.is_authenticated or request.user.username != 'UNICLUBSADMIN':
        django_messages.error(request, "Only Admin can add events.")
        return redirect('home')
    if request.method == 'POST':
        form = EventForm(request.POST, request.FILES)
        if form.is_valid():
            event = form.save(commit=False)
            event.is_approved = True  # Admin added events are auto-approved
            event.save()
            django_messages.success(request, 'Event added successfully!')
            return redirect('home')
    else:
        form = EventForm()
    return render(request, 'app/event_form.html', {'form': form, 'title': 'Add New Event'})


def event_edit(request, pk):
    if not request.user.is_authenticated or request.user.username != 'UNICLUBSADMIN':
        django_messages.error(request, "Only Admin can edit events.")
        return redirect('home')
    event = get_object_or_404(Event, pk=pk)
    if request.method == 'POST':
        form = EventForm(request.POST, request.FILES, instance=event)
        if form.is_valid():
            form.save()
            django_messages.success(request, 'Event updated successfully!')
            return redirect('club_admin')
    else:
        form = EventForm(instance=event)
    return render(request, 'app/event_form.html', {'form': form, 'title': 'Edit Event', 'event': event})


def event_delete(request, pk):
    if not request.user.is_authenticated or request.user.username != 'UNICLUBSADMIN':
        django_messages.error(request, "Only Admin can delete events.")
        return redirect('home')
    event = get_object_or_404(Event, pk=pk)
    if request.method == 'POST':
        event.delete()
        django_messages.success(request, 'Event deleted.')
        return redirect('club_admin')
    return render(request, 'app/confirm_delete.html', {'object': event, 'type': 'Event', 'cancel_url': 'club_admin'})


def event_approve(request, pk):
    event = get_object_or_404(Event, pk=pk)
    event.is_approved = True
    event.save()
    django_messages.success(request, f'"{event.title}" has been approved.')
    return redirect('system_admin')


def event_detail(request, pk):
    event = get_object_or_404(Event, pk=pk)
    ratings = EventRating.objects.filter(event=event)
    avg_rating = None
    if ratings.exists():
        avg_rating = round(sum(r.score for r in ratings) / ratings.count(), 1)
    reg_form = EventRegistrationForm(initial={'event': event})
    return render(request, 'app/event_detail.html', {
        'event': event,
        'ratings': ratings,
        'avg_rating': avg_rating,
        'reg_form': reg_form,
    })


# ─────────────────────────────────────
# EVENT ARCHIVE (ratings)
# ─────────────────────────────────────
def event_archive(request):
    past_events = Event.objects.filter(status='past', is_approved=True)
    rating_form = EventRatingForm()
    if request.method == 'POST':
        rating_form = EventRatingForm(request.POST)
        if rating_form.is_valid():
            rating = rating_form.save(commit=False)
            # Automatically find or create a Student record for the logged-in user
            student, _ = Student.objects.get_or_create(
                full_name=request.user.username,
                defaults={'student_id': request.user.id, 'department': 'General', 'email': request.user.email}
            )
            rating.student = student
            try:
                rating.save()
                django_messages.success(request, 'Rating submitted successfully!')
            except Exception:
                django_messages.error(request, 'You have already rated this event.')
            return redirect('event_archive')
    return render(request, 'app/event_archive.html', {
        'past_events': past_events,
        'rating_form': rating_form,
    })


# ─────────────────────────────────────
# STUDENTS CRUD
# ─────────────────────────────────────
def student_list(request):
    students = Student.objects.all()
    return render(request, 'app/student_list.html', {'students': students})


def student_add(request):
    if request.method == 'POST':
        form = StudentForm(request.POST)
        if form.is_valid():
            form.save()
            django_messages.success(request, 'Student registered successfully!')
            return redirect('system_admin')
    else:
        form = StudentForm()
    return render(request, 'app/student_form.html', {'form': form, 'title': 'Add New Student'})


def student_edit(request, pk):
    student = get_object_or_404(Student, pk=pk)
    if request.method == 'POST':
        form = StudentForm(request.POST, instance=student)
        if form.is_valid():
            form.save()
            django_messages.success(request, 'Student updated!')
            return redirect('system_admin')
    else:
        form = StudentForm(instance=student)
    return render(request, 'app/student_form.html', {'form': form, 'title': 'Edit Student', 'student': student})


def student_delete(request, pk):
    student = get_object_or_404(Student, pk=pk)
    if request.method == 'POST':
        student.delete()
        django_messages.success(request, 'Student deleted.')
        return redirect('system_admin')
    return render(request, 'app/confirm_delete.html', {'object': student, 'type': 'Student', 'cancel_url': 'system_admin'})


# ─────────────────────────────────────
# MEMBERSHIP REQUESTS
# ─────────────────────────────────────
def membership_requests_view(request):
    pending = MembershipRequest.objects.filter(status='pending')
    return render(request, 'app/membership_requests.html', {'requests': pending})


def membership_approve(request, pk):
    req = get_object_or_404(MembershipRequest, pk=pk)
    req.status = 'approved'
    req.reviewed_at = timezone.now()
    req.save()
    django_messages.success(request, f'{req.student.full_name} approved for {req.club.name}.')
    return redirect('club_admin')


def membership_reject(request, pk):
    req = get_object_or_404(MembershipRequest, pk=pk)
    req.status = 'rejected'
    req.reviewed_at = timezone.now()
    req.save()
    django_messages.warning(request, f'{req.student.full_name} rejected from {req.club.name}.')
    return redirect('club_admin')


@login_required
def membership_apply(request):
    if request.method == 'POST':
        form = MembershipRequestForm(request.POST)
        if form.is_valid():
            form.save()
            django_messages.success(request, 'Membership request submitted!')
            return redirect('dashboard')
    else:
        form = MembershipRequestForm()
    return render(request, 'app/membership_form.html', {'form': form, 'title': 'Apply for Membership'})


# ─────────────────────────────────────
# EVENT REGISTRATIONS
# ─────────────────────────────────────
@login_required
def event_register(request, pk):
    event = get_object_or_404(Event, pk=pk)
    if request.method == 'POST':
        form = EventRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            django_messages.success(request, f'Registered for "{event.title}" successfully!')
            return redirect('dashboard')
    else:
        form = EventRegistrationForm(initial={'event': event})
    return render(request, 'app/registration_form.html', {'form': form, 'event': event})


def registration_approve(request, pk):
    reg = get_object_or_404(EventRegistration, pk=pk)
    reg.status = 'approved'
    reg.save()
    django_messages.success(request, f'{reg.student.full_name} registration approved.')
    return redirect('club_admin')


def registration_reject(request, pk):
    reg = get_object_or_404(EventRegistration, pk=pk)
    reg.status = 'rejected'
    reg.save()
    django_messages.warning(request, f'{reg.student.full_name} registration rejected.')
    return redirect('club_admin')


# ─────────────────────────────────────
# ANNOUNCEMENTS CRUD
# ─────────────────────────────────────
def announcements(request):
    ann_list = Announcement.objects.filter(is_published=True)
    return render(request, 'app/announcements.html', {'announcements': ann_list})


def announcement_add(request):
    if not request.user.is_authenticated or request.user.username != 'UNICLUBSADMIN':
        django_messages.error(request, "Only Admin can add announcements.")
        return redirect('home')
    if request.method == 'POST':
        form = AnnouncementForm(request.POST)
        if form.is_valid():
            form.save()
            django_messages.success(request, 'Announcement published!')
            return redirect('announcements')
    else:
        form = AnnouncementForm()
    return render(request, 'app/announcement_form.html', {'form': form, 'title': 'New Announcement'})


def announcement_edit(request, pk):
    if not request.user.is_authenticated or request.user.username != 'UNICLUBSADMIN':
        django_messages.error(request, "Only Admin can edit announcements.")
        return redirect('home')
    ann = get_object_or_404(Announcement, pk=pk)
    if request.method == 'POST':
        form = AnnouncementForm(request.POST, instance=ann)
        if form.is_valid():
            form.save()
            django_messages.success(request, 'Announcement updated!')
            return redirect('announcements')
    else:
        form = AnnouncementForm(instance=ann)
    return render(request, 'app/announcement_form.html', {'form': form, 'title': 'Edit Announcement', 'announcement': ann})


def announcement_delete(request, pk):
    if not request.user.is_authenticated or request.user.username != 'UNICLUBSADMIN':
        django_messages.error(request, "Only Admin can delete announcements.")
        return redirect('home')
    ann = get_object_or_404(Announcement, pk=pk)
    if request.method == 'POST':
        ann.delete()
        django_messages.success(request, 'Announcement deleted.')
        return redirect('announcements')
    return render(request, 'app/confirm_delete.html', {'object': ann, 'type': 'Announcement', 'cancel_url': 'announcements'})


def announcement_detail(request, pk):
    ann = get_object_or_404(Announcement, pk=pk)
    return render(request, 'app/announcement_detail.html', {'announcement': ann})


# ─────────────────────────────────────
# MESSAGES
# ─────────────────────────────────────
@login_required
def messages_view(request):
    clubs = Club.objects.filter(is_active=True)
    selected_club = None
    chat_messages = []
    club_id = request.GET.get('club')
    if club_id:
        selected_club = get_object_or_404(Club, pk=club_id)
        chat_messages = Message.objects.filter(receiver_club=selected_club)
        Message.objects.filter(receiver_club=selected_club, is_read=False).update(is_read=True)

    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            msg = form.save(commit=False)
            msg.sender_name = request.user.username
            msg.save()
            django_messages.success(request, 'Message sent!')
            club_id = request.POST.get('receiver_club', '')
            return redirect(f'/messages/?club={club_id}')
        else:
            django_messages.error(request, "Error sending message. Please check the content.")
    else:
        form = MessageForm()
    return render(request, 'app/messages.html', {
        'clubs': clubs,
        'selected_club': selected_club,
        'chat_messages': chat_messages,
        'form': form,
    })


# ─────────────────────────────────────
# CLUB INFO (edit from club panel)
# ─────────────────────────────────────
def club_info(request, pk):
    club = get_object_or_404(Club, pk=pk)
    if request.method == 'POST':
        form = ClubForm(request.POST, request.FILES, instance=club)
        if form.is_valid():
            form.save()
            django_messages.success(request, 'Club info updated!')
            return redirect('club_admin')
    else:
        form = ClubForm(instance=club)
    return render(request, 'app/club_form.html', {'form': form, 'title': 'Edit Club Info', 'club': club})


# ─────────────────────────────────────
# CORE TEAM APPLICATIONS
# ─────────────────────────────────────
@login_required
def core_team_apply(request, pk):
    club = get_object_or_404(Club, pk=pk)
    if not club.is_core_team_recruiting:
        django_messages.error(request, "This club is not currently recruiting for Core Team.")
        return redirect('club_detail', pk=pk)
    
    if request.method == 'POST':
        form = CoreTeamApplicationForm(request.POST)
        if form.is_valid():
            app = form.save(commit=False)
            
            # Robust student retrieval
            student = Student.objects.filter(student_id=str(request.user.id)).first()
            if not student:
                student = Student.objects.filter(email=request.user.email).first()
            
            if not student:
                student = Student.objects.create(
                    student_id=str(request.user.id),
                    full_name=request.user.username,
                    department='General',
                    email=request.user.email or f"{request.user.username}@university.edu"
                )
            
            app.student = student
            app.club = club
            app.save()
            django_messages.success(request, f"Your application for {app.department} Core Team submitted!")
            return redirect('club_detail', pk=pk)
    else:
        form = CoreTeamApplicationForm()
    
    return render(request, 'app/core_team_form.html', {'form': form, 'club': club})


def core_team_approve(request, pk):
    app = get_object_or_404(CoreTeamApplication, pk=pk)
    app.status = 'approved'
    app.save()
    django_messages.success(request, f"{app.student.full_name} approved for {app.department} Core Team.")
    return redirect('club_admin')


def core_team_reject(request, pk):
    app = get_object_or_404(CoreTeamApplication, pk=pk)
    app.status = 'rejected'
    app.save()
    django_messages.warning(request, f"{app.student.full_name} rejected for {app.department} Core Team.")
    return redirect('club_admin')
