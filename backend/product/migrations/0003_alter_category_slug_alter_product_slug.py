# Generated by Django 4.1.4 on 2023-11-01 07:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0002_rename_numreviews_product_total_reviews_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='slug',
            field=models.SlugField(blank=True, default='', max_length=400),
        ),
        migrations.AlterField(
            model_name='product',
            name='slug',
            field=models.CharField(blank=True, default='', max_length=300),
        ),
    ]