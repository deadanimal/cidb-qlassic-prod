# Generated by Django 2.2.10 on 2020-11-02 06:55

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('trainings', '0008_remove_registrationtraining_payment'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='training',
            name='from_date',
        ),
        migrations.RemoveField(
            model_name='training',
            name='to_date',
        ),
    ]
