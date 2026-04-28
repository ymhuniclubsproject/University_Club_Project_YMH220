# -*- coding: utf-8 -*-
from django import forms
from .models import Club, Student, Event, MembershipRequest, EventRegistration, EventRating, Announcement, Message, CoreTeamApplication


class ClubForm(forms.ModelForm): # Form for club registration and management with admin credentials | Kulüp kaydı ve yönetimi için admin yetkili form
    admin_username = forms.CharField(max_length=150, required=False, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Admin Username'}))
    admin_password = forms.CharField(max_length=128, required=False, widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Admin Password'}))

    class Meta:
        model = Club
        fields = ['name', 'description', 'category', 'logo', 'leader', 'is_recruiting', 'is_core_team_recruiting']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Club Name'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Club description...'}),
            'category': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. Technology, Arts, Sports'}),
            'logo': forms.FileInput(attrs={'class': 'form-control-file'}),
            'leader': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Club Leader Name'}),
            'is_recruiting': forms.CheckboxInput(attrs={'class': 'form-check-input ml-2'}),
            'is_core_team_recruiting': forms.CheckboxInput(attrs={'class': 'form-check-input ml-2'}),
        }


class StudentForm(forms.ModelForm): # Handles student profile creation and academic info | Öğrenci profili oluşturma ve akademik bilgi girişini yönetir
    class Meta:
        model = Student
        fields = ['full_name', 'student_id', 'department', 'faculty', 'grade', 'email', 'year']
        widgets = {
            'full_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Full Name'}),
            'student_id': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Student ID'}),
            'department': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Department'}),
            'faculty': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Faculty'}),
            'grade': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Grade (e.g. 1st Year, 2nd Year)'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'}),
            'year': forms.NumberInput(attrs={'class': 'form-control', 'min': 1, 'max': 6}),
        }


FACULTY_CHOICES = [ # List of university faculties | Üniversite fakülte listesi
    ('', '--- Select Faculty ---'),
    ('Diş Hekimliği Fakültesi', 'Diş Hekimliği Fakültesi'),
    ('Eczacılık Fakültesi', 'Eczacılık Fakültesi'),
    ('Eğitim Fakültesi', 'Eğitim Fakültesi'),
    ('Fen Fakültesi', 'Fen Fakültesi'),
    ('İktisadi ve İdari Bilimler Fakültesi', 'İktisadi ve İdari Bilimler Fakültesi'),
    ('İlahiyat Fakültesi', 'İlahiyat Fakültesi'),
    ('İletişim Fakültesi', 'İletişim Fakültesi'),
    ('İnsani ve Sosyal Bilimler Fakültesi', 'İnsani ve Sosyal Bilimler Fakültesi'),
    ('Mimarlık Fakültesi', 'Mimarlık Fakültesi'),
    ('Mühendislik Fakültesi', 'Mühendislik Fakültesi'),
    ('Sağlık Bilimleri Fakültesi', 'Sağlık Bilimleri Fakültesi'),
    ('Spor Bilimleri Fakültesi', 'Spor Bilimleri Fakültesi'),
    ('Su Ürünleri Fakültesi', 'Su Ürünleri Fakültesi'),
    ('Teknoloji Fakültesi', 'Teknoloji Fakültesi'),
    ('Tıp Fakültesi', 'Tıp Fakültesi'),
    ('Veteriner Fakültesi', 'Veteriner Fakültesi'),
]

GRADE_CHOICES = [ # Grade levels for students | Öğrenciler için sınıf seviyeleri
    ('', '--- Select Grade ---'),
    ('Hazırlık', 'Hazırlık'),
    ('1. Sınıf', '1. Sınıf'),
    ('2. Sınıf', '2. Sınıf'),
    ('3. Sınıf', '3. Sınıf'),
    ('4. Sınıf', '4. Sınıf'),
    ('Lisansüstü', 'Lisansüstü'),
]

DEPARTMENT_CHOICES_UNI = [ # Predefined university departments | Tanımlı üniversite bölümleri
    ('', '--- Select Department ---'),
    ('Yazılım Mühendisliği', 'Yazılım Mühendisliği'),
    ('Bilgisayar Mühendisliği', 'Bilgisayar Mühendisliği'),
    ('Adli Bilişim Mühendisliği', 'Adli Bilişim Mühendisliği'),
    ('Elektrik-Elektronik Mühendisliği', 'Elektrik-Elektronik Mühendisliği'),
    ('Makine Mühendisliği', 'Makine Mühendisliği'),
    ('İnşaat Mühendisliği', 'İnşaat Mühendisliği'),
    ('Mekatronik Mühendisliği', 'Mekatronik Mühendisliği'),
    ('Tıp', 'Tıp'),
    ('Diş Hekimliği', 'Diş Hekimliği'),
    ('Hemşirelik', 'Hemşirelik'),
    ('Beslenme ve Diyetetik', 'Beslenme ve Diyetetik'),
    ('İşletme', 'İşletme'),
    ('İktisat', 'İktisat'),
    ('Siyaset Bilimi ve Kamu Yönetimi', 'Siyaset Bilimi ve Kamu Yönetimi'),
    ('İlahiyat', 'İlahiyat'),
    ('Türkçe Öğretmenliği', 'Türkçe Öğretmenliği'),
    ('Sınıf Öğretmenliği', 'Sınıf Öğretmenliği'),
    ('Diğer', 'Diğer'),
]

class CoreTeamApplicationForm(forms.ModelForm): # Form for core team recruitment applications | Çekirdek ekip alımı başvuruları için form
    full_name = forms.CharField(max_length=200, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Full Name'}))
    department_name = forms.ChoiceField(choices=DEPARTMENT_CHOICES_UNI, widget=forms.Select(attrs={'class': 'form-control'}))
    faculty = forms.ChoiceField(choices=FACULTY_CHOICES, widget=forms.Select(attrs={'class': 'form-control'}))
    grade = forms.ChoiceField(choices=GRADE_CHOICES, widget=forms.Select(attrs={'class': 'form-control'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'}))

    class Meta:
        model = CoreTeamApplication
        fields = ['department']
        widgets = {
            'department': forms.Select(attrs={'class': 'form-control'}),
        }


class EventForm(forms.ModelForm): # Form for creating and updating club events | Kulüp etkinlikleri oluşturma ve güncelleme formu
    class Meta:
        model = Event
        fields = ['title', 'description', 'club', 'location', 'event_date', 'event_time', 'max_participants', 'image']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Event Title'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Event description...'}),
            'club': forms.Select(attrs={'class': 'form-control'}),
            'location': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Location'}),
            'event_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'event_time': forms.TimeInput(attrs={'class': 'form-control', 'type': 'time'}),
            'max_participants': forms.NumberInput(attrs={'class': 'form-control', 'min': 1}),
            'image': forms.FileInput(attrs={'class': 'form-control-file'}),
        }


class MembershipRequestForm(forms.Form): # Data collection for club membership applications | Kulüp üyelik başvuruları için veri toplama formu
    full_name = forms.CharField(max_length=200, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Full Name'}))
    department = forms.ChoiceField(choices=DEPARTMENT_CHOICES_UNI, widget=forms.Select(attrs={'class': 'form-control'}))
    faculty = forms.ChoiceField(choices=FACULTY_CHOICES, widget=forms.Select(attrs={'class': 'form-control'}))
    grade = forms.ChoiceField(choices=GRADE_CHOICES, widget=forms.Select(attrs={'class': 'form-control'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'}))
    club_id = forms.IntegerField(widget=forms.HiddenInput(), required=False)


class EventRegistrationForm(forms.Form): # Data collection for joining specific events | Belirli etkinliklere katılım için veri toplama formu
    full_name = forms.CharField(max_length=200, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Full Name'}))
    department = forms.ChoiceField(choices=DEPARTMENT_CHOICES_UNI, widget=forms.Select(attrs={'class': 'form-control'}))
    faculty = forms.ChoiceField(choices=FACULTY_CHOICES, widget=forms.Select(attrs={'class': 'form-control'}))
    grade = forms.ChoiceField(choices=GRADE_CHOICES, widget=forms.Select(attrs={'class': 'form-control'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'}))
    event_id = forms.IntegerField(widget=forms.HiddenInput(), required=False)


class EventRatingForm(forms.ModelForm): # Collects scores and feedback for events | Etkinlikler için puan ve geri bildirim toplar
    class Meta:
        model = EventRating
        fields = ['event', 'score', 'comment']
        widgets = {
            'event': forms.Select(attrs={'class': 'form-control'}),
            'score': forms.Select(attrs={'class': 'form-control'}),
            'comment': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Write your comment...'}),
        }


class AnnouncementForm(forms.ModelForm): # Manages announcements with dynamic field visibility for admins | Adminler için dinamik alan görünürlüğü ile duyuru yönetimi
    departments = forms.MultipleChoiceField(
        choices=CoreTeamApplication.DEPARTMENT_CHOICES,
        widget=forms.CheckboxSelectMultiple,
        required=False,
        label="Target Departments (for Core Team)"
    )

    class Meta:
        model = Announcement
        fields = ['title', 'content', 'announcement_type', 'club']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Announcement Title'}),
            'content': forms.Textarea(attrs={'class': 'form-control', 'rows': 5, 'placeholder': 'Announcement content...'}),
            'announcement_type': forms.Select(attrs={'class': 'form-control'}),
            'club': forms.Select(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if user and hasattr(user, 'managed_club') and user.username != 'UNICLUBSADMIN':
            self.fields['announcement_type'].widget = forms.HiddenInput()
            self.fields['club'].widget = forms.HiddenInput()
            self.fields['announcement_type'].required = False
            self.fields['club'].required = False


class MessageForm(forms.ModelForm): # Handles direct messaging to clubs | Kulüplere doğrudan mesaj gönderimini yönetir
    class Meta:
        model = Message
        fields = ['sender_name', 'receiver_club', 'content']
        widgets = {
            'sender_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Your Name / Club Name'}),
            'receiver_club': forms.Select(attrs={'class': 'form-control'}),
            'content': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Type your message...'}),
        }

    def __init__(self, *args, **kwargs):
        super(MessageForm, self).__init__(*args, **kwargs)
        self.fields['sender_name'].required = False


from django.contrib.auth.models import User

class UserRegistrationForm(forms.ModelForm): # Handles new user sign-ups with password confirmation | Şifre onayı ile yeni kullanıcı kayıtlarını yönetir
    username = forms.CharField(max_length=150, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'}))
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Confirm Password'}))

    class Meta:
        model = User
        fields = ['username', 'password']

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password != confirm_password:
            raise forms.ValidationError("Passwords do not match")
        return cleaned_data

class LoginForm(forms.Form): # Standard login credentials form | Standart giriş bilgileri formu
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'}))

class ProfileEditForm(forms.Form): # Form for updating existing student profile details | Mevcut öğrenci profili detaylarını güncelleme formu
    full_name = forms.CharField(max_length=200, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Full Name'}))
    department = forms.ChoiceField(choices=DEPARTMENT_CHOICES_UNI, widget=forms.Select(attrs={'class': 'form-control'}))
    faculty = forms.ChoiceField(choices=FACULTY_CHOICES, widget=forms.Select(attrs={'class': 'form-control'}))
    grade = forms.ChoiceField(choices=GRADE_CHOICES, widget=forms.Select(attrs={'class': 'form-control'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'}))