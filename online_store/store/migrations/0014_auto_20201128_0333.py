# Generated by Django 3.1.3 on 2020-11-28 02:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0013_auto_20201127_0724'),
    ]

    operations = [
        migrations.RenameField(
            model_name='shippingaddress',
            old_name='address',
            new_name='address1',
        ),
        migrations.RenameField(
            model_name='shippingaddress',
            old_name='zipcode',
            new_name='address2',
        ),
        migrations.AddField(
            model_name='shippingaddress',
            name='zip_code',
            field=models.CharField(max_length=200, null=True),
        ),
    ]
