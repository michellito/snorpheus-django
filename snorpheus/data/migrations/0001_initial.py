# Generated by Django 3.2.16 on 2022-11-05 23:39

import django.core.files.storage
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('portal', '0005_alter_sleepsession_true_start_time'),
    ]

    operations = [
        migrations.CreateModel(
            name='SleepSessionAudio',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_time', models.DateTimeField()),
                ('audio_file', models.FileField(storage=django.core.files.storage.FileSystemStorage(location='/media/audio'), upload_to='')),
                ('sleep_session', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sleep_session', to='portal.sleepsession')),
            ],
            options={
                'verbose_name': 'Sleep Session Audio',
                'ordering': ('-pk',),
            },
        ),
    ]