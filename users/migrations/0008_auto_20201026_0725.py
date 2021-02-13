# Generated by Django 2.2.10 on 2020-10-26 07:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0007_auto_20201026_0713'),
    ]

    operations = [
        migrations.AddField(
            model_name='academicqualification',
            name='modified_by',
            field=models.CharField(max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='academicqualification',
            name='created_by',
            field=models.CharField(max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='academicqualification',
            name='institution',
            field=models.CharField(max_length=50, null=True, verbose_name='Name of institution'),
        ),
        migrations.AlterField(
            model_name='academicqualification',
            name='program',
            field=models.CharField(max_length=50, null=True, verbose_name='Academic program'),
        ),
        migrations.AlterField(
            model_name='academicqualification',
            name='qualification',
            field=models.CharField(choices=[('spm', 'SPM'), ('diploma', 'Diploma'), ('degree', 'Degree'), ('master', 'Master'), ('phd', 'PHD')], max_length=20, null=True),
        ),
        migrations.AlterField(
            model_name='academicqualification',
            name='year',
            field=models.IntegerField(null=True, verbose_name='Graduation year'),
        ),
    ]
