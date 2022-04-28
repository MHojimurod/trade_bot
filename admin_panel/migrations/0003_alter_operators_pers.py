# Generated by Django 4.0.3 on 2022-04-28 17:45

from django.db import migrations
import multiselectfield.db.fields


class Migration(migrations.Migration):

    dependencies = [
        ('admin_panel', '0002_support_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='operators',
            name='pers',
            field=multiselectfield.db.fields.MultiSelectField(choices=[('statistic', 'Statistika'), ('operators', 'Operatorlar'), ('category', 'Kategoriya'), ('ads', 'Reklama'), ('fillial', 'Filliallar'), ('present', 'Aksiyalar'), ('settings', 'Bot Sozlamalari'), ('text', 'Textlar'), ('followers', 'Foydalanuvchilar'), ('comments', 'Kommentariyalar')], max_length=81),
        ),
    ]
