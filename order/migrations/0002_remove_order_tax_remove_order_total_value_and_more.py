# Generated by Django 4.2.4 on 2023-08-28 09:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='tax',
        ),
        migrations.RemoveField(
            model_name='order',
            name='total_value',
        ),
        migrations.AddField(
            model_name='orderitem',
            name='tax',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10),
        ),
        migrations.AddField(
            model_name='orderitem',
            name='total_value',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10),
        ),
    ]
