# Generated by Django 2.2.10 on 2021-03-29 16:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('billings', '0009_auto_20210324_1654'),
    ]

    operations = [
        migrations.AlterField(
            model_name='payment',
            name='payment_status',
            field=models.CharField(choices=[('2', 'Pending Authorization (Applicable for B2B model)'), ('1', 'Successful'), ('0', 'Fail'), ('-1', 'Pending')], default='-1', max_length=15),
        ),
    ]
