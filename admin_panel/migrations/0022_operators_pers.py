# Generated by Django 4.0.3 on 2022-04-19 15:44

from django.db import migrations
import multiselectfield.db.fields


class Migration(migrations.Migration):

    dependencies = [
        ('admin_panel', '0021_remove_operators_name_remove_operators_password_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='operators',
            name='pers',
            field=multiselectfield.db.fields.MultiSelectField(choices=[('cashier', 'Кассир'), ('order', 'Заказ'), ('menu', 'Меню'), ('statistic', 'Статистика'), ('map', 'Карта'), ('Ad', 'Рассылки'), ('fillial', 'Филиалы'), ('users', 'Пользователи'), ('followers', 'Подписчики'), ('settings_bot', 'Настройки бота'), ('history', 'История заказов'), ('comments', 'Комментарии')], default=[], max_length=89),
            preserve_default=False,
        ),
    ]
