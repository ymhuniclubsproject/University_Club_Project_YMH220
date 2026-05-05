from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User


class Club(models.Model): # Stores club profile, recruitment status, and admin links | Kulüp profili, alım durumu ve admin bağlantılarını tutar
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    logo = models.ImageField(upload_to='club_logos/', blank=True, null=True)
    category = models.CharField(max_length=100, blank=True)
    is_active = models.BooleanField(default=True)
    is_approved = models.BooleanField(default=False)
    is_recruiting = models.BooleanField(default=False)
    is_core_team_recruiting = models.BooleanField(default=False)
    leader = models.CharField(max_length=200, blank=True, null=True, help_text="Name of the club leader")
    created_at = models.DateTimeField(default=timezone.now)
    admin_user = models.OneToOneField(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='managed_club')

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['-created_at']


class Student(models.Model): # Base model for student academic and contact information | Öğrenci akademik ve iletişim bilgileri için temel model
    full_name = models.CharField(max_length=200)
    student_id = models.CharField(max_length=20, unique=True)
    department = models.CharField(max_length=200)
    faculty = models.CharField(max_length=200, blank=True, null=True)
    grade = models.CharField(max_length=50, blank=True, null=True)
    email = models.EmailField(unique=True)
    year = models.IntegerField(default=1)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.full_name

    class Meta:
        ordering = ['-created_at']


class CoreTeamApplication(models.Model): # Manages applications for specialized club management roles | Uzmanlaşmış kulüp yönetim rolleri için başvuruları yönetir
    DEPARTMENT_CHOICES = [
        ('Event', 'Event'),
        ('Design', 'Design'),
        ('Sponsorship', 'Sponsorship'),
        ('Project', 'Project'),
        ('Social Media', 'Social Media'),
        ('Coordinator', 'Coordinator'),
    ]
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ]
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='core_team_apps')
    club = models.ForeignKey(Club, on_delete=models.CASCADE, related_name='core_team_apps')
    department = models.CharField(max_length=50, choices=DEPARTMENT_CHOICES)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    applied_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.student.full_name} -> {self.club.name} ({self.department})"


class Event(models.Model): # Event definition with logic for attendance and average ratings | Katılım ve ortalama puanlama mantığıyla etkinlik tanımı
    STATUS_CHOICES = [
        ('upcoming', 'Upcoming'),
        ('ongoing', 'Ongoing'),
        ('past', 'Past'),
    ]
    title = models.CharField(max_length=200)
    description = models.TextField()
    club = models.ForeignKey(Club, on_delete=models.CASCADE, related_name='events')
    location = models.CharField(max_length=200, blank=True)
    event_date = models.DateField()
    event_time = models.TimeField(blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='upcoming')
    is_approved = models.BooleanField(default=False)
    max_participants = models.IntegerField(default=100)
    image = models.ImageField(upload_to='event_images/', blank=True, null=True)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.title

    @property
    def average_rating(self):
        ratings = self.ratings.all()
        if not ratings:
            return 0
        return round(sum(r.score for r in ratings) / ratings.count(), 1)

    @property
    def star_rating(self):
        avg = self.average_rating
        full_stars = int(avg)
        half_star = 1 if (avg - full_stars) >= 0.5 else 0
        return range(full_stars), range(half_star), range(5 - full_stars - half_star)

    class Meta:
        ordering = ['-event_date']


class MembershipRequest(models.Model): # Links students to clubs for general membership | Genel üyelik için öğrencileri kulüplere bağlar
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ]
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='membership_requests')
    club = models.ForeignKey(Club, on_delete=models.CASCADE, related_name='membership_requests')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    applied_at = models.DateTimeField(default=timezone.now)
    reviewed_at = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return f"{self.student.full_name} -> {self.club.name}"

    class Meta:
        ordering = ['-applied_at']


class EventRegistration(models.Model): # Tracks student registration and attendance status for events | Etkinlikler için öğrenci kayıt ve katılım durumunu takip eder
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ]
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='event_registrations')
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='registrations')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    registered_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.student.full_name} -> {self.event.title}"


class EventRating(models.Model): # Collects numeric scores and comments for completed events | Tamamlanan etkinlikler için sayısal puan ve yorum toplar
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='ratings')
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='ratings')
    score = models.IntegerField(choices=[(i, str(i)) for i in range(1, 6)])
    comment = models.TextField(blank=True)
    rated_at = models.DateTimeField(default=timezone.now)

    class Meta:
        unique_together = ('event', 'student')

    def __str__(self):
        return f"{self.event.title} - {self.score}/5"


class Announcement(models.Model): # General or targeted broadcast messages for users | Kullanıcılar için genel veya hedefli duyuru mesajları
    TYPE_CHOICES = [
        ('school', 'School'),
        ('club', 'Club'),
        ('general', 'General'),
        ('core_team', 'Core Team Recruitment'),
    ]
    title = models.CharField(max_length=200)
    content = models.TextField()
    announcement_type = models.CharField(max_length=20, choices=TYPE_CHOICES, default='general')
    club = models.ForeignKey(Club, on_delete=models.SET_NULL, null=True, blank=True, related_name='announcements')
    is_core_team = models.BooleanField(default=False)
    is_published = models.BooleanField(default=True)
    published_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-published_at']


class Message(models.Model): # Handles direct communication between guests/students and clubs | Ziyaretçi/öğrenciler ile kulüpler arası doğrudan iletişimi sağlar
    sender_name = models.CharField(max_length=200)
    receiver_club = models.ForeignKey(Club, on_delete=models.CASCADE, related_name='received_messages')
    content = models.TextField()
    sent_at = models.DateTimeField(default=timezone.now)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.sender_name}: {self.content[:50]}"

    class Meta:
        ordering = ['sent_at']