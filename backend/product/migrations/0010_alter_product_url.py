# Generated by Django 4.2.7 on 2024-02-20 17:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0009_product_url_alter_product_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='url',
            field=models.CharField(blank=True, max_length=1000),
        ),
    ]