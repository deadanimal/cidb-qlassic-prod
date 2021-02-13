# Generated by Django 2.2.10 on 2020-11-16 10:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('assessments', '0027_auto_20201111_0434'),
    ]

    operations = [
        migrations.AlterField(
            model_name='qlassicassessmentapplication',
            name='application_status',
            field=models.CharField(blank=True, choices=[('pending', 'Pending'), ('reviewed', 'Reviewed'), ('verified', 'Verified'), ('rejected', 'Rejected'), ('rejected_amendment', 'Rejected (With Amendment)'), ('need_payment', 'Need Payment'), ('paid', 'Paid'), ('assessor_assign', 'Assessor Assign'), ('confirm', 'Confirm'), ('in_progress', 'In-Progress'), ('completed', 'Completed'), ('approved', 'Approved')], max_length=10, null=True),
        ),
    ]
