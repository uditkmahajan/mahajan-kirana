# Generated by Django 4.2.7 on 2024-02-05 06:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0011_order_order_list'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='order_list',
            field=models.ImageField(blank=True, null=True, upload_to='orderlist/'),
        ),
    ]
