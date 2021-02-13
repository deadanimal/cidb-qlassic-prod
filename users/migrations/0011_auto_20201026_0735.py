# Generated by Django 2.2.10 on 2020-10-26 07:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0010_auto_20201026_0733'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='trainer',
            name='trainer_number',
        ),
        migrations.AddField(
            model_name='trainer',
            name='created_by',
            field=models.CharField(max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='trainer',
            name='modified_by',
            field=models.CharField(max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='trainer',
            name='trainer_no',
            field=models.CharField(blank=True, max_length=6, verbose_name='Trainer number'),
        ),
        migrations.AlterField(
            model_name='assessor',
            name='assessor_no',
            field=models.CharField(blank=True, max_length=6, verbose_name='Assessor number'),
        ),
    ]
