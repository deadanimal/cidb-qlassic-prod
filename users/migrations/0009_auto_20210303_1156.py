# Generated by Django 2.2.10 on 2021-03-03 03:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0008_auto_20210224_1206'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='icno',
            field=models.CharField(max_length=12, null=True, verbose_name="Identity Card Number (without '-')"),
        ),
    ]
