# Generated by Django 4.2.4 on 2023-08-28 09:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cart', '0005_remove_cart_created_at_remove_cart_status'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cart',
            name='total_price',
        ),
        migrations.AddField(
            model_name='cartitem',
            name='tax',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10),
        ),
    ]
