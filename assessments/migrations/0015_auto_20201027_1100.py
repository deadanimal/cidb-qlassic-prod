# Generated by Django 2.2.10 on 2020-10-27 11:00

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('assessments', '0014_siteattendance'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='siteattendance',
            name='ad',
        ),
        migrations.RemoveField(
            model_name='siteattendance',
            name='report_number',
        ),
        migrations.RemoveField(
            model_name='siteattendance',
            name='type_of_report',
        ),
    ]
