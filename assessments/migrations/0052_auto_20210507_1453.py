# Generated by Django 2.2.10 on 2021-05-07 06:53

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('assessments', '0051_scope'),
    ]

    operations = [
        migrations.AlterField(
            model_name='scope',
            name='scope',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=200), blank=True, default=[1, 2, 3], size=None),
            preserve_default=False,
        ),
    ]
