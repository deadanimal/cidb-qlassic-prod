# Generated by Django 2.2.10 on 2020-12-16 07:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('trainings', '0022_remove_training_publish'),
    ]

    operations = [
        migrations.AddField(
            model_name='training',
            name='publish',
            field=models.BooleanField(default=False, verbose_name='Published?'),
        ),
    ]
