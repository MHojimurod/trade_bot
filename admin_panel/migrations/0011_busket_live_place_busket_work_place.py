# Generated by Django 4.0.3 on 2022-06-30 16:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('admin_panel', '0010_support_media_type'),
    ]

    operations = [
        migrations.AddField(
            model_name='busket',
            name='live_place',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='busket',
            name='work_place',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
