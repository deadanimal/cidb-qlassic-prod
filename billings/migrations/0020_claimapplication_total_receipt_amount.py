# Generated by Django 2.2.10 on 2021-01-15 11:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('billings', '0019_auto_20210115_1935'),
    ]

    operations = [
        migrations.AddField(
            model_name='claimapplication',
            name='total_receipt_amount',
            field=models.DecimalField(decimal_places=2, max_digits=20, null=True, verbose_name='Amount'),
        ),
    ]
