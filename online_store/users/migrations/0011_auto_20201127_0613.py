# Generated by Django 3.1.3 on 2020-11-27 05:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0010_auto_20201125_1251'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='address2',
            field=models.CharField(blank=True, default='-', max_length=100, null=True),
        ),
    ]