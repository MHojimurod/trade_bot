# Generated by Django 4.0.3 on 2022-05-05 11:41

import ckeditor.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('admin_panel', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='desc_ru',
            field=ckeditor.fields.RichTextField(blank=True, default=''),
        ),
        migrations.AddField(
            model_name='product',
            name='desc_uz',
            field=ckeditor.fields.RichTextField(blank=True, default=''),
        ),
    ]