# Generated by Django 3.1.3 on 2020-12-06 04:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0017_delete_customer'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='category',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
