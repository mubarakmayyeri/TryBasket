# Generated by Django 4.1.3 on 2022-11-26 22:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0007_product_product_offer'),
    ]

    operations = [
        migrations.AddField(
            model_name='variation',
            name='price_multiplier',
            field=models.IntegerField(default=1),
        ),
    ]
