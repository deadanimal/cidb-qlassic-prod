# Generated by Django 2.2.10 on 2020-11-03 06:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('trainings', '0013_auto_20201103_0242'),
    ]

    operations = [
        migrations.AlterField(
            model_name='training',
            name='state',
            field=models.CharField(choices=[('ME', 'Melaka'), ('JH', 'Johor'), ('NS', 'Negeri Sembilan'), ('PH', 'Pahang'), ('TE', 'Terengganu'), ('KN', 'Kelantan'), ('PK', 'Perak'), ('PL', 'Perlis'), ('KH', 'Kedah'), ('SL', 'Selangor'), ('KL', 'Kuala Lumpur'), ('SA', 'Sabah'), ('SW', 'Sarawak'), ('PG', 'Pulau Pinang')], max_length=255, null=True),
        ),
    ]
