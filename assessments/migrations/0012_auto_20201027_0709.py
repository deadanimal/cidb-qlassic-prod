# Generated by Django 2.2.10 on 2020-10-27 07:09

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('assessments', '0011_auto_20201027_0656'),
    ]

    operations = [
        migrations.RenameField(
            model_name='assessmentdata',
            old_name='apron_parameter_drain',
            new_name='apron_perimeter_drain',
        ),
        migrations.RemoveField(
            model_name='assessmentdata',
            name='carpark_carporch',
        ),
        migrations.RemoveField(
            model_name='assessmentdata',
            name='defect_group',
        ),
        migrations.RemoveField(
            model_name='assessmentdata',
            name='external_works',
        ),
        migrations.RemoveField(
            model_name='assessmentdata',
            name='picture',
        ),
        migrations.RemoveField(
            model_name='assessmentdata',
            name='qlassic_score_mockup',
        ),
        migrations.AddField(
            model_name='assessmentdata',
            name='car_park',
            field=models.FloatField(null=True, verbose_name='Car park/ Car porch'),
        ),
        migrations.AddField(
            model_name='assessmentdata',
            name='created_by',
            field=models.CharField(max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='assessmentdata',
            name='dg',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='assessments.DefectGroup'),
        ),
        migrations.AddField(
            model_name='assessmentdata',
            name='mock_up_score',
            field=models.FloatField(null=True, verbose_name='QLASSIC score with mock up'),
        ),
        migrations.AddField(
            model_name='assessmentdata',
            name='modified_by',
            field=models.CharField(max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='assessmentdata',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='assessmentdata',
            name='assessor',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='users.Assessor'),
        ),
        migrations.AlterField(
            model_name='assessmentdata',
            name='block',
            field=models.IntegerField(null=True, verbose_name="Block's name"),
        ),
        migrations.AlterField(
            model_name='assessmentdata',
            name='count_circulation',
            field=models.IntegerField(null=True, verbose_name='Number of circulation samples'),
        ),
        migrations.AlterField(
            model_name='assessmentdata',
            name='count_principle',
            field=models.IntegerField(null=True, verbose_name='Number of principles samples'),
        ),
        migrations.AlterField(
            model_name='assessmentdata',
            name='count_sampling_done',
            field=models.IntegerField(null=True, verbose_name='Number of sampling done'),
        ),
        migrations.AlterField(
            model_name='assessmentdata',
            name='count_services',
            field=models.IntegerField(null=True, verbose_name='Number of services samples'),
        ),
        migrations.AlterField(
            model_name='assessmentdata',
            name='element',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='assessments.Element'),
        ),
        migrations.AlterField(
            model_name='assessmentdata',
            name='material_functional_test',
            field=models.FloatField(null=True, verbose_name='Material & Functional Test'),
        ),
        migrations.AlterField(
            model_name='assessmentdata',
            name='me_fittings',
            field=models.FloatField(null=True, verbose_name='Basic M&E Fittings'),
        ),
        migrations.AlterField(
            model_name='assessmentdata',
            name='qaa',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='assessments.QlassicAssessmentApplication'),
        ),
        migrations.AlterField(
            model_name='assessmentdata',
            name='qlassic_score',
            field=models.FloatField(null=True, verbose_name='QLASSIC score'),
        ),
        migrations.AlterField(
            model_name='assessmentdata',
            name='time',
            field=models.TimeField(null=True, verbose_name='Time taken to complete data for one sample'),
        ),
        migrations.AlterField(
            model_name='assessmentdata',
            name='total',
            field=models.FloatField(null=True, verbose_name='Total (1.1-5)'),
        ),
        migrations.AlterField(
            model_name='assessmentdata',
            name='unit',
            field=models.IntegerField(null=True, verbose_name='Unit number'),
        ),
    ]
