# Generated by Django 4.2.7 on 2023-12-23 16:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('User', '0005_alter_user_area_alter_user_city_alter_user_email_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='notifications',
            field=models.IntegerField(default=0),
        ),
    ]
