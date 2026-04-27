# -*- coding: utf-8 -*-
from django import forms
from .models import Club, Student, Event, MembershipRequest, EventRegistration, EventRating, Announcement, Message, CoreTeamApplication


class ClubForm(forms.ModelForm):
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


class StudentForm(forms.ModelForm):
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


class CoreTeamApplicationForm(forms.ModelForm):
    class Meta:
        model = CoreTeamApplication
        fields = ['department']
        widgets = {
            'department': forms.Select(attrs={'class': 'form-control'}),
        }


class EventForm(forms.ModelForm):
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


class MembershipRequestForm(forms.ModelForm):
    class Meta:
        model = MembershipRequest
        fields = ['student', 'club']
        widgets = {
            'student': forms.Select(attrs={'class': 'form-control'}),
            'club': forms.Select(attrs={'class': 'form-control'}),
        }


class EventRegistrationForm(forms.ModelForm):
    class Meta:
        model = EventRegistration
        fields = ['student', 'event']
        widgets = {
            'student': forms.Select(attrs={'class': 'form-control'}),
            'event': forms.Select(attrs={'class': 'form-control'}),
        }


class EventRatingForm(forms.ModelForm):
    class Meta:
        model = EventRating
        fields = ['event', 'student', 'score', 'comment']
        widgets = {
            'event': forms.Select(attrs={'class': 'form-control'}),
            'student': forms.Select(attrs={'class': 'form-control'}),
            'score': forms.Select(attrs={'class': 'form-control'}),
            'comment': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Write your comment...'}),
        }


class AnnouncementForm(forms.ModelForm):
    class Meta:
        model = Announcement
        fields = ['title', 'content', 'announcement_type', 'club']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Announcement Title'}),
            'content': forms.Textarea(attrs={'class': 'form-control', 'rows': 5, 'placeholder': 'Announcement content...'}),
            'announcement_type': forms.Select(attrs={'class': 'form-control'}),
            'club': forms.Select(attrs={'class': 'form-control'}),
        }


class MessageForm(forms.ModelForm):
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

class UserRegistrationForm(forms.ModelForm):
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

class LoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'}))
