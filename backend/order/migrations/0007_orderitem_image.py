# Generated by Django 4.2.7 on 2023-12-20 06:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0006_remove_orderitem_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='orderitem',
            name='image',
            field=models.URLField(default=None),
        ),
    ]