# Generated by Django 3.1.3 on 2020-12-09 15:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0019_product_featured'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='featured',
            field=models.BooleanField(blank=True, default='False', null=True),
        ),
    ]