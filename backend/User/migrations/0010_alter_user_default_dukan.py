# Generated by Django 4.2.7 on 2024-03-10 16:00

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('dukandar', '0002_alter_apnidukan_delivery_detail'),
        ('User', '0009_alter_user_default_dukan'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='default_dukan',
            field=models.ForeignKey(blank=True, default='1', on_delete=django.db.models.deletion.DO_NOTHING, to='dukandar.apnidukan'),
        ),
    ]