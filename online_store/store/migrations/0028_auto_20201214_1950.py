# Generated by Django 3.1.3 on 2020-12-14 18:50

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0027_auto_20201213_0528'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='date_order',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]
