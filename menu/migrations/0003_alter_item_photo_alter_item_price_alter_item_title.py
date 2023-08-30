# Generated by Django 4.2.4 on 2023-08-28 22:03

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('menu', '0002_item_is_visible'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='photo',
            field=models.ImageField(blank=True, null=True, upload_to='images/images'),
        ),
        migrations.AlterField(
            model_name='item',
            name='price',
            field=models.DecimalField(decimal_places=2, max_digits=10, validators=[django.core.validators.MinValueValidator(0.01)]),
        ),
        migrations.AlterField(
            model_name='item',
            name='title',
            field=models.CharField(max_length=100, unique=True),
        ),
    ]