# Generated by Django 4.0.5 on 2022-07-17 18:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('onlinestore', '0016_alter_cartitems_quantity'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cartitems',
            name='quantity',
            field=models.IntegerField(default=1),
        ),
    ]