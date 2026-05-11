from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_remove_event_image_url_club_logo_event_image'),
    ]

    operations = [
        migrations.AddField( # Indicates if the club is currently accepting new members | Kulübün yeni üye alımı yapıp yapmadığını belirtir
            model_name='club',
            name='is_recruiting',
            field=models.BooleanField(default=False),
        ),
    ]