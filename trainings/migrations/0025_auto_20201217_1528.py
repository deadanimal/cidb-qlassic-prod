# Generated by Django 2.2.10 on 2020-12-17 07:28

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('trainings', '0024_auto_20201217_1517'),
    ]

    operations = [
        migrations.RenameField(
            model_name='registrationtraining',
            old_name='user',
            new_name='trainer',
        ),
    ]
