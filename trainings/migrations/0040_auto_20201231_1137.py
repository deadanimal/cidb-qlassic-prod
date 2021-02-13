# Generated by Django 2.2.10 on 2020-12-31 03:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('trainings', '0039_auto_20201231_1028'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='registrationtraining',
            name='registration_type',
        ),
        migrations.AlterField(
            model_name='registrationtraining',
            name='created_by',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='registrationtraining',
            name='modified_by',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='registrationtraining',
            name='payment_mode',
            field=models.CharField(choices=[('on', 'On'), ('off', 'Off')], default=True, max_length=5, null=True),
        ),
    ]
