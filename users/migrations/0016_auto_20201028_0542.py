# Generated by Django 2.2.10 on 2020-10-28 05:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0015_auto_20201028_0541'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='greencard_exp_date',
            field=models.DateTimeField(null=True, verbose_name="Green card's expired date"),
        ),
    ]
