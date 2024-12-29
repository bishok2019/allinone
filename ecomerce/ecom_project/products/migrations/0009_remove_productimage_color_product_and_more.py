# Generated by Django 5.1.4 on 2024-12-28 06:10

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0008_remove_productimage_product_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='productimage',
            name='color_product',
        ),
        migrations.AddField(
            model_name='productimage',
            name='product',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='product_images', to='products.product'),
        ),
        migrations.AddField(
            model_name='productvariant',
            name='product_color_image',
            field=models.ImageField(null=True, upload_to='product'),
        ),
    ]
