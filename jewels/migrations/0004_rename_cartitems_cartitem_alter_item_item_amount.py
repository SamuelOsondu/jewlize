# Generated by Django 4.1.2 on 2022-11-12 20:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jewels', '0003_cart_customer_shippingaddress_cartitems_and_more'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='CartItems',
            new_name='CartItem',
        ),
        migrations.AlterField(
            model_name='item',
            name='item_amount',
            field=models.FloatField(max_length=20),
        ),
    ]
