# Generated by Django 2.2.10 on 2021-01-29 02:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('trainings', '0048_auto_20210122_1742'),
    ]

    operations = [
        migrations.AlterField(
            model_name='registrationtraining',
            name='participant_designation',
            field=models.CharField(max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='registrationtraining',
            name='participant_organization',
            field=models.CharField(max_length=200, null=True),
        ),
    ]
