# Generated by Django 3.1.3 on 2020-12-09 14:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0018_product_category'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='featured',
            field=models.BooleanField(default='False'),
        ),
    ]
