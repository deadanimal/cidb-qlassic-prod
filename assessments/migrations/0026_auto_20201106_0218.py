# Generated by Django 2.2.10 on 2020-11-06 02:18

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('assessments', '0025_auto_20201104_0917'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='qlassicassessmentapplication',
            name='approved_by',
        ),
        migrations.RemoveField(
            model_name='qlassicassessmentapplication',
            name='approved_date',
        ),
        migrations.RemoveField(
            model_name='qlassicassessmentapplication',
            name='remarks3',
        ),
    ]
