from django.db import migrations

class Migration(migrations.Migration):

    dependencies = [
        ('tracker', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='musicplayer',
            name='duration',
        ),
    ] 