# Generated by Django 2.2.10 on 2020-12-14 10:08

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('assessments', '0038_auto_20201214_1528'),
    ]

    operations = [
        migrations.AlterField(
            model_name='supportingdocuments',
            name='at',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='trainings.ApplicationTrainer'),
        ),
        migrations.AlterField(
            model_name='supportingdocuments',
            name='jt',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='trainings.JoinedTraining'),
        ),
        migrations.AlterField(
            model_name='supportingdocuments',
            name='qaa',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='assessments.QlassicAssessmentApplication'),
        ),
    ]
