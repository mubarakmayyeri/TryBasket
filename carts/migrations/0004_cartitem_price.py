# Generated by Django 4.1.3 on 2022-11-28 18:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('carts', '0003_cartitem_user_alter_cartitem_cart'),
    ]

    operations = [
        migrations.AddField(
            model_name='cartitem',
            name='price',
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
    ]
