# Generated by Django 2.2.10 on 2023-02-13 10:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0008_projectinfo_parent_obj'),
    ]

    operations = [
        migrations.AddField(
            model_name='projectinfo',
            name='value',
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
    ]
