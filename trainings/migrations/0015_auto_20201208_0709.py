# Generated by Django 2.2.10 on 2020-12-08 07:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('trainings', '0014_auto_20201103_0617'),
    ]

    operations = [
        migrations.AlterField(
            model_name='registrationtraining',
            name='participant_hpno',
            field=models.CharField(max_length=15, null=True, verbose_name="Participant's phone number"),
        ),
    ]
