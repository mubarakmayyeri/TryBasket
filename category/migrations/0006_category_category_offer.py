# Generated by Django 4.1.3 on 2022-11-25 19:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('category', '0005_alter_category_cat_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='category_offer',
            field=models.IntegerField(null=True),
        ),
    ]