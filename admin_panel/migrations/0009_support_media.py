# Generated by Django 4.0.3 on 2022-06-28 09:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('admin_panel', '0008_alter_operators_photo'),
    ]

    operations = [
        migrations.AddField(
            model_name='support',
            name='media',
            field=models.FileField(blank=True, null=True, upload_to=''),
        ),
    ]
