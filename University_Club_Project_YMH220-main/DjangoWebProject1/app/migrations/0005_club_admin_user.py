import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0004_club_is_core_team_recruiting_club_leader_and_more'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField( # Links a unique system user as the club administrator | Kulüp yöneticisi olarak benzersiz bir sistem kullanıcısı atar
            model_name='club',
            name='admin_user',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='managed_club', to=settings.AUTH_USER_MODEL),
        ),
    ]