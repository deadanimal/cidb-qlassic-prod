# Generated by Django 2.2.10 on 2020-12-10 06:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('billings', '0015_auto_20201208_1404'),
    ]

    operations = [
        migrations.AlterField(
            model_name='claimapplication',
            name='date_of_transaction',
            field=models.DateField(null=True, verbose_name='Date of Transaction'),
        ),
    ]
