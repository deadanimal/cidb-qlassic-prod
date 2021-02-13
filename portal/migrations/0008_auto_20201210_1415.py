# Generated by Django 2.2.10 on 2020-12-10 06:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('portal', '0007_auto_20201102_0658'),
    ]

    operations = [
        migrations.AlterField(
            model_name='announcement',
            name='announcement',
            field=models.TextField(max_length=3000, null=True),
        ),
        migrations.AlterField(
            model_name='publication',
            name='publication',
            field=models.TextField(max_length=3000, null=True),
        ),
        migrations.AlterField(
            model_name='training',
            name='from_date',
            field=models.DateField(null=True, verbose_name='From Date)'),
        ),
        migrations.AlterField(
            model_name='training',
            name='to_date',
            field=models.DateField(null=True, verbose_name='To Date'),
        ),
    ]
