# Generated by Django 2.2.10 on 2021-02-13 13:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('billings', '0004_auto_20210213_2157'),
    ]

    operations = [
        migrations.AlterField(
            model_name='payment',
            name='payment_date',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
