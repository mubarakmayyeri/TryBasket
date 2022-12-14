# Generated by Django 4.1.3 on 2022-11-15 17:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0003_remove_order_address_order_address_line1_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='payment',
            name='paid',
        ),
        migrations.AddField(
            model_name='payment',
            name='payment_method',
            field=models.CharField(default='', max_length=100),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='payment',
            name='status',
            field=models.BooleanField(default=False),
            preserve_default=False,
        ),
    ]
