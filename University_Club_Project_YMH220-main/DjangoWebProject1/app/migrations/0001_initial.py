import django.db.models.deletion
import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Club', # Creates the club management table | Kulüp yönetim tablosunu oluşturur
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('description', models.TextField(blank=True)),
                ('category', models.CharField(blank=True, max_length=100)),
                ('is_active', models.BooleanField(default=True)),
                ('is_approved', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
            ],
            options={
                'ordering': ['-created_at'],
            },
        ),
        migrations.CreateModel(
            name='Student', # Stores student information and profiles | Öğrenci bilgilerini ve profillerini tutar
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('full_name', models.CharField(max_length=200)),
                ('student_id', models.CharField(max_length=20, unique=True)),
                ('department', models.CharField(max_length=200)),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('year', models.IntegerField(default=1)),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
            ],
            options={
                'ordering': ['-created_at'],
            },
        ),
        migrations.CreateModel(
            name='Announcement', # Manages school or club announcements | Okul veya kulüp duyurularını yönetir
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('content', models.TextField()),
                ('announcement_type', models.CharField(choices=[('school', 'School'), ('club', 'Club'), ('general', 'General')], default='general', max_length=20)),
                ('is_published', models.BooleanField(default=True)),
                ('published_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('club', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='announcements', to='app.club')),
            ],
            options={
                'ordering': ['-published_at'],
            },
        ),
        migrations.CreateModel(
            name='Event', # Defines club events and activities | Kulüp etkinliklerini ve aktivitelerini tanımlar
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('description', models.TextField()),
                ('location', models.CharField(blank=True, max_length=200)),
                ('event_date', models.DateField()),
                ('event_time', models.TimeField(blank=True, null=True)),
                ('status', models.CharField(choices=[('upcoming', 'Upcoming'), ('ongoing', 'Ongoing'), ('past', 'Past')], default='upcoming', max_length=20)),
                ('is_approved', models.BooleanField(default=False)),
                ('max_participants', models.IntegerField(default=100)),
                ('image_url', models.URLField(blank=True)),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('club', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='events', to='app.club')),
            ],
            options={
                'ordering': ['-event_date'],
            },
        ),
        migrations.CreateModel(
            name='Message', # Handles messaging between users and clubs | Kullanıcılar ve kulüpler arası mesajlaşmayı sağlar
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sender_name', models.CharField(max_length=200)),
                ('content', models.TextField()),
                ('sent_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('is_read', models.BooleanField(default=False)),
                ('receiver_club', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='received_messages', to='app.club')),
            ],
            options={
                'ordering': ['sent_at'],
            },
        ),
        migrations.CreateModel(
            name='MembershipRequest', # Tracks student applications for clubs | Kulüp üyelik başvurularını takip eder
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(choices=[('pending', 'Pending'), ('approved', 'Approved'), ('rejected', 'Rejected')], default='pending', max_length=20)),
                ('applied_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('reviewed_at', models.DateTimeField(blank=True, null=True)),
                ('club', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='membership_requests', to='app.club')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='membership_requests', to='app.student')),
            ],
            options={
                'ordering': ['-applied_at'],
            },
        ),
        migrations.CreateModel(
            name='EventRegistration', # Manages student sign-ups for events | Etkinliklere öğrenci kayıtlarını yönetir
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(choices=[('pending', 'Pending'), ('approved', 'Approved'), ('rejected', 'Rejected')], default='pending', max_length=20)),
                ('registered_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('event', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='registrations', to='app.event')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='event_registrations', to='app.student')),
            ],
        ),
        migrations.CreateModel(
            name='EventRating', # Stores event ratings and comments | Etkinlik puanlarını ve yorumlarını tutar
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('score', models.IntegerField(choices=[(1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5')])),
                ('comment', models.TextField(blank=True)),
                ('rated_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('event', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ratings', to='app.event')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ratings', to='app.student')),
            ],
            options={
                'unique_together': {('event', 'student')},
            },
        ),
    ]