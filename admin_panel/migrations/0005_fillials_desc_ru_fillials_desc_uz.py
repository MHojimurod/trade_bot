# Generated by Django 4.0.3 on 2022-04-22 19:44

import ckeditor.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('admin_panel', '0004_remove_fillials_desc_ru_f_remove_fillials_desc_uz_f'),
    ]

    operations = [
        migrations.AddField(
            model_name='fillials',
            name='desc_ru',
            field=ckeditor.fields.RichTextField(default='a'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='fillials',
            name='desc_uz',
            field=ckeditor.fields.RichTextField(default='sdf'),
            preserve_default=False,
        ),
    ]
