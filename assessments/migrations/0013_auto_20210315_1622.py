# Generated by Django 2.2.10 on 2021-03-15 08:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('assessments', '0012_auto_20210315_1257'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='element',
            name='sub_component_weightage',
        ),
        migrations.AddField(
            model_name='element',
            name='category_weightage',
            field=models.BooleanField(choices=[(True, 'Yes'), (False, 'No (Default)')], default=False, null=True, verbose_name='Use As Category Weightage'),
        ),
        migrations.AddField(
            model_name='element',
            name='weightage_a',
            field=models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=8, null=True, verbose_name='Weightage A'),
        ),
        migrations.AddField(
            model_name='element',
            name='weightage_b',
            field=models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=8, null=True, verbose_name='Weightage B'),
        ),
        migrations.AddField(
            model_name='element',
            name='weightage_c',
            field=models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=8, null=True, verbose_name='Weightage C'),
        ),
        migrations.AddField(
            model_name='element',
            name='weightage_d',
            field=models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=8, null=True, verbose_name='Weightage D'),
        ),
        migrations.AlterField(
            model_name='element',
            name='weightage',
            field=models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=8, null=True, verbose_name='Weightage'),
        ),
    ]
