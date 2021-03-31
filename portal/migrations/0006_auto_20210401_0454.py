# Generated by Django 2.2.10 on 2021-03-31 20:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('portal', '0005_auto_20210218_1309'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lettertemplate',
            name='template_type',
            field=models.CharField(choices=[('qlassic_score_letter', 'QLASSIC Score letter'), ('qlassic_certificate', 'QLASSIC Certificate'), ('qlassic_report', 'QLASSIC Report'), ('attendance_sheet', 'Attendance Sheet'), ('trainer_interview_letter', 'Trainer Interview Letter'), ('trainer_reject_letter', 'Trainer Rejection Letter'), ('trainer_accreditation_letter', 'Trainer Accreditation Letter'), ('qca_interview_letter', 'QCA Interview Letter'), ('qca_reject_letter', 'QCA Rejection Letter'), ('qca_accreditation_letter', 'QCA Accreditation Letter'), ('qca_accreditation_certificate', 'QCA Accreditation Certificate'), ('qia_accreditation_certificate', 'QIA Accreditation Certificate')], max_length=150, null=True),
        ),
    ]
