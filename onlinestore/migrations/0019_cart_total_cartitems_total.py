# Generated by Django 4.0.5 on 2022-07-18 08:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('onlinestore', '0018_checkout_delete_delivery'),
    ]

    operations = [
        migrations.AddField(
            model_name='cart',
            name='total',
            field=models.IntegerField(null=True),
        ),
        migrations.AddField(
            model_name='cartitems',
            name='total',
            field=models.IntegerField(null=True),
        ),
    ]