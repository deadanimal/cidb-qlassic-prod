# Generated by Django 2.2.10 on 2020-12-08 08:38

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0022_auto_20201208_0709'),
    ]

    operations = [
        migrations.RenameField(
            model_name='verifiedcontractor',
            old_name='user_id',
            new_name='user',
        ),
    ]
