# Generated by Django 2.2.10 on 2020-10-23 11:59

import core.helpers
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('assessments', '0004_auto_20201023_1159'),
        ('trainings', '0002_auto_20201020_0645'),
    ]

    operations = [
        migrations.CreateModel(
            name='File',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('upload', models.FileField(null=True, upload_to=core.helpers.PathAndRename('cidb-qlassic/documents'))),
                ('name', models.CharField(max_length=255)),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('modified_date', models.DateTimeField(auto_now=True)),
                ('at', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to='trainings.ApplicationTrainer')),
                ('jt', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to='trainings.JoinedTraining')),
                ('qaa', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to='assessments.QlassicAssessmentApplication')),
            ],
        ),
    ]
