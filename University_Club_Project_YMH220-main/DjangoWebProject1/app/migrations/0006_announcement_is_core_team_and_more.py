from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0005_club_admin_user'),
    ]

    operations = [
        migrations.AddField( # Flags if the announcement is specifically for core team recruitment | Duyurunun çekirdek ekip alımıyla ilgili olup olmadığını işaretler
            model_name='announcement',
            name='is_core_team',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField( # Adds core team recruitment to announcement category choices | Duyuru türü seçeneklerine çekirdek ekip alımını ekler
            model_name='announcement',
            name='announcement_type',
            field=models.CharField(choices=[('school', 'School'), ('club', 'Club'), ('general', 'General'), ('core_team', 'Core Team Recruitment')], default='general', max_length=20),
        ),
        migrations.AlterField( # Defines specific functional departments for core team roles | Çekirdek ekip rolleri için belirli fonksiyonel departmanları tanımlar
            model_name='coreteamapplication',
            name='department',
            field=models.CharField(choices=[('Event', 'Event'), ('Design', 'Design'), ('Sponsorship', 'Sponsorship'), ('Project', 'Project'), ('Social Media', 'Social Media'), ('Coordinator', 'Coordinator')], max_length=50),
        ),
    ]