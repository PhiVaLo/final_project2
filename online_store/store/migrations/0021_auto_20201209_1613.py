# Generated by Django 3.1.3 on 2020-12-09 15:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0020_auto_20201209_1613'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='featured',
            field=models.BooleanField(blank=True, default=False, null=True),
        ),
    ]