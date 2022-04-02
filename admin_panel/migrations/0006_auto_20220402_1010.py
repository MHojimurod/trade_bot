# Generated by Django 3.2.9 on 2022-04-02 10:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('admin_panel', '0005_alter_botsettings_money'),
    ]

    operations = [
        migrations.AddField(
            model_name='operators',
            name='photo',
            field=models.ImageField(default='/static/images/default.png', upload_to='images/'),
        ),
        migrations.AddField(
            model_name='operators',
            name='surname',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='operators',
            name='name',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]
