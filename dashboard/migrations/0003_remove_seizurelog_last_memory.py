# Generated by Django 5.0.6 on 2024-10-14 06:07

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0002_sportlog_sport_time'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='seizurelog',
            name='last_memory',
        ),
    ]
