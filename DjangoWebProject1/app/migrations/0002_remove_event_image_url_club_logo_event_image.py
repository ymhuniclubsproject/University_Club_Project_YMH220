from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField( # Removes URL-based image field from Event | Event modelinden URL tabanlı resim alanını kaldırır
            model_name='event',
            name='image_url',
        ),
        migrations.AddField( # Adds file upload support for club logos | Kulüp logoları için dosya yükleme desteği ekler
            model_name='club',
            name='logo',
            field=models.ImageField(blank=True, null=True, upload_to='club_logos/'),
        ),
        migrations.AddField( # Adds file upload support for event images | Etkinlik görselleri için dosya yükleme desteği ekler
            model_name='event',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='event_images/'),
        ),
    ]