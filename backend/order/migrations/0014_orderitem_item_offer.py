# Generated by Django 4.2.7 on 2024-02-23 11:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0013_remove_orderitem_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='orderitem',
            name='item_offer',
            field=models.CharField(blank=True, default='', max_length=1000),
        ),
    ]
