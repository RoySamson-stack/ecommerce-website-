# Generated by Django 4.0.5 on 2022-07-17 11:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('onlinestore', '0009_alter_cartitems_quantity'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cartitems',
            name='quantity',
            field=models.IntegerField(default=1),
        ),
    ]