# Generated by Django 4.1.3 on 2022-11-15 17:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0004_remove_payment_paid_payment_payment_method_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='payment',
            name='status',
            field=models.BooleanField(default=False),
        ),
    ]