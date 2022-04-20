# Generated by Django 4.0.3 on 2022-04-19 16:05

from django.db import migrations
import multiselectfield.db.fields


class Migration(migrations.Migration):

    dependencies = [
        ('admin_panel', '0022_operators_pers'),
    ]

    operations = [
        migrations.AlterField(
            model_name='operators',
            name='pers',
            field=multiselectfield.db.fields.MultiSelectField(choices=[('order', 'Buyurtmalar'), ('statistic', 'Statistika'), ('operators', 'Operatorlar'), ('category', 'Kategoriya'), ('Ad', 'Рассылки'), ('fillial', 'Filliallar'), ('settings', 'Bot Sozlamalari'), ('followers', 'Foydalanuvchilar')], max_length=64),
        ),
    ]
