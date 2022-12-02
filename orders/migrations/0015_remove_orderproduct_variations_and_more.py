# Generated by Django 4.1.3 on 2022-12-02 00:44

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0008_variation_price_multiplier'),
        ('orders', '0014_alter_orderproduct_order'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='orderproduct',
            name='variations',
        ),
        migrations.AddField(
            model_name='orderproduct',
            name='variations',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='shop.variation'),
        ),
    ]
