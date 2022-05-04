# Generated by Django 4.0.3 on 2022-05-04 12:31

import admin_panel.models
import ckeditor.fields
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import multiselectfield.db.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Ads',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('photo', models.ImageField(upload_to='images/')),
                ('desc', ckeditor.fields.RichTextField()),
            ],
        ),
        migrations.CreateModel(
            name='Aksiya',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name_uz', models.CharField(max_length=15)),
                ('name_ru', models.CharField(max_length=15)),
                ('mode', models.IntegerField(choices=[(0, 'text'), (1, 'image'), (2, 'video')])),
                ('media', models.FileField(blank=True, null=True, upload_to='')),
                ('caption', models.TextField()),
                ('is_active', models.BooleanField(default=True)),
            ],
            bases=(models.Model, admin_panel.models.Name),
        ),
        migrations.CreateModel(
            name='BotSettings',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('money', models.IntegerField(default=0)),
                ('request_self_image', models.ImageField(upload_to='')),
                ('request_passport_image', models.ImageField(upload_to='')),
                ('request_self_passport_image', models.ImageField(upload_to='')),
            ],
        ),
        migrations.CreateModel(
            name='Busket',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bis_ordered', models.BooleanField(default=False)),
                ('order_time', models.DateTimeField(blank=True, null=True)),
                ('self_image', models.ImageField(blank=True, null=True, upload_to='busket')),
                ('passport_image', models.ImageField(blank=True, null=True, upload_to='busket')),
                ('self_password_image', models.ImageField(blank=True, null=True, upload_to='busket')),
                ('extra_number', models.CharField(blank=True, max_length=20, null=True)),
                ('comment', models.TextField(blank=True, null=True)),
                ('status', models.IntegerField(choices=[(0, 'Kutilmoqda'), (1, 'Qabul qilindi'), (2, 'Rad etildi'), (3, 'Tasdiqlandi!'), (4, 'Tasdiqlanmadi'), (5, 'Arxiv')], default=0)),
            ],
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name_uz', models.CharField(max_length=200)),
                ('name_ru', models.CharField(max_length=200)),
                ('active', models.BooleanField(default=False)),
                ('parent', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='admin_panel.category')),
            ],
        ),
        migrations.CreateModel(
            name='Color',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('color', models.CharField(max_length=200)),
                ('base_percent', models.PositiveIntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Fillials',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name_uz', models.CharField(max_length=200)),
                ('name_ru', models.CharField(max_length=200)),
                ('desc_uz', ckeditor.fields.RichTextField()),
                ('desc_ru', ckeditor.fields.RichTextField()),
                ('active', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='Language',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('code', models.CharField(max_length=3, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('chat_id', models.IntegerField()),
                ('name', models.CharField(max_length=200)),
                ('number', models.CharField(max_length=200)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('filial', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='admin_panel.fillials')),
                ('language', models.ForeignKey(on_delete=models.SET(1), to='admin_panel.language')),
            ],
        ),
        migrations.CreateModel(
            name='Text',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('data', models.TextField()),
                ('language', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='admin_panel.language')),
            ],
        ),
        migrations.CreateModel(
            name='Support',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('data', models.TextField(blank=True)),
                ('status', models.BooleanField(default=False)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='admin_panel.user')),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name_uz', models.CharField(max_length=200)),
                ('name_ru', models.CharField(max_length=200)),
                ('photo', models.ImageField(upload_to='images/')),
                ('active', models.BooleanField(default=False)),
                ('tan_price', models.IntegerField()),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='admin_panel.category')),
                ('color', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='admin_panel.color')),
            ],
        ),
        migrations.CreateModel(
            name='Percent',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('months', models.IntegerField()),
                ('percent', models.IntegerField()),
                ('color', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='admin_panel.color')),
            ],
        ),
        migrations.CreateModel(
            name='Operators',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('surname', models.CharField(max_length=100)),
                ('username', models.CharField(max_length=100)),
                ('phone', models.IntegerField()),
                ('photo', models.ImageField(default='/static/dashboard/assets/img/default.png', upload_to='images/')),
                ('region', models.CharField(blank=True, max_length=200, null=True)),
                ('address', models.CharField(blank=True, max_length=200, null=True)),
                ('active', models.BooleanField(default=False)),
                ('is_have', models.BooleanField(default=False)),
                ('pers', multiselectfield.db.fields.MultiSelectField(choices=[('statistic', 'Statistika'), ('operators', 'Operatorlar'), ('category', 'Kategoriya'), ('ads', 'Reklama'), ('fillial', 'Filliallar'), ('present', 'Aksiyalar'), ('settings', 'Bot Sozlamalari'), ('text', 'Textlar'), ('followers', 'Foydalanuvchilar'), ('comments', 'Kommentariyalar')], max_length=81)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Location',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('latitude', models.FloatField()),
                ('longitude', models.FloatField()),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='admin_panel.user')),
            ],
        ),
        migrations.CreateModel(
            name='BusketItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('_count', models.IntegerField()),
                ('busket', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='admin_panel.busket')),
                ('month', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='admin_panel.percent')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='admin_panel.product')),
            ],
        ),
        migrations.AddField(
            model_name='busket',
            name='actioner',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='actioner', to='admin_panel.operators'),
        ),
        migrations.AddField(
            model_name='busket',
            name='location',
            field=models.ForeignKey(blank=True, null=True, on_delete=models.SET(None), to='admin_panel.location'),
        ),
        migrations.AddField(
            model_name='busket',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='admin_panel.user'),
        ),
    ]
