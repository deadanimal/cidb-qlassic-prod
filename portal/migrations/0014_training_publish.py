# Generated by Django 2.2.10 on 2020-12-16 07:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('portal', '0013_auto_20201216_1501'),
    ]

    operations = [
        migrations.AddField(
            model_name='training',
            name='publish',
            field=models.BooleanField(default=False),
        ),
    ]
