# Generated by Django 4.0.5 on 2022-07-19 08:06

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('onlinestore', '0021_remove_cart_total_remove_cartitems_total'),
    ]

    operations = [
        migrations.RenameField(
            model_name='checkout',
            old_name='payment_data',
            new_name='phone_number',
        ),
        migrations.RemoveField(
            model_name='checkout',
            name='payment_method',
        ),
    ]