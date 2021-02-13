# Generated by Django 2.2.10 on 2020-12-21 13:55

import core.helpers
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('assessments', '0041_auto_20201216_1501'),
    ]

    operations = [
        migrations.CreateModel(
            name='ElementResult',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('created_by', models.CharField(max_length=50, null=True)),
                ('modified_date', models.DateTimeField(auto_now=True)),
                ('modified_by', models.CharField(max_length=50, null=True)),
                ('assessment_data', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='assessments.AssessmentData')),
            ],
        ),
        migrations.AddField(
            model_name='element',
            name='element_type',
            field=models.CharField(choices=[('architectural_works', 'Architectural Works'), ('external_works', 'External Works')], max_length=5, null=True),
        ),
        migrations.CreateModel(
            name='ElementResultDocument',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('file_name', models.CharField(max_length=255, null=True)),
                ('file', models.FileField(max_length=255, null=True, upload_to=core.helpers.PathAndRename('results'))),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('created_by', models.CharField(max_length=50, null=True)),
                ('modified_date', models.DateTimeField(auto_now=True)),
                ('modified_by', models.CharField(max_length=50, null=True)),
                ('element_result', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='assessments.ElementResult')),
            ],
        ),
        migrations.AddField(
            model_name='elementresult',
            name='element',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='assessments.Element'),
        ),
        migrations.CreateModel(
            name='DefectGroupResult',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('checked', models.BooleanField(default=False)),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('created_by', models.CharField(max_length=50, null=True)),
                ('modified_date', models.DateTimeField(auto_now=True)),
                ('modified_by', models.CharField(max_length=50, null=True)),
                ('assessment_data', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='assessments.AssessmentData')),
                ('defect_group', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='assessments.DefectGroup')),
            ],
        ),
    ]
