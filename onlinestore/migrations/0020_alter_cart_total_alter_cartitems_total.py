# Generated by Django 4.0.5 on 2022-07-18 08:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('onlinestore', '0019_cart_total_cartitems_total'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cart',
            name='total',
            field=models.IntegerField(default=0, null=True),
        ),
        migrations.AlterField(
            model_name='cartitems',
            name='total',
            field=models.IntegerField(default=0, null=True),
        ),
    ]
