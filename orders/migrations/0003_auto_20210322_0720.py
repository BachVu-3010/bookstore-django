# Generated by Django 3.1.5 on 2021-03-22 07:20

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0002_auto_20210322_0235'),
    ]

    operations = [
        migrations.RenameField(
            model_name='order',
            old_name='payment_method',
            new_name='paymentMethod',
        ),
        migrations.RenameField(
            model_name='order',
            old_name='total_price',
            new_name='totalPrice',
        ),
    ]
