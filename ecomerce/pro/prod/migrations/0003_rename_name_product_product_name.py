# Generated by Django 5.1.4 on 2024-12-30 10:30

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('prod', '0002_product_image_product_product_description_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='product',
            old_name='name',
            new_name='product_name',
        ),
    ]
