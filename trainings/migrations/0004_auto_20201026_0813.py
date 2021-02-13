# Generated by Django 2.2.10 on 2020-10-26 08:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('trainings', '0003_auto_20201026_0731'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='registrationtraining',
            name='participant',
        ),
        migrations.RemoveField(
            model_name='training',
            name='type_training',
        ),
        migrations.AddField(
            model_name='registrationtraining',
            name='amount',
            field=models.CharField(blank=True, max_length=4),
        ),
        migrations.AddField(
            model_name='registrationtraining',
            name='created_by',
            field=models.CharField(max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='registrationtraining',
            name='modified_by',
            field=models.CharField(max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='registrationtraining',
            name='participant_email',
            field=models.CharField(blank=True, max_length=20, verbose_name="Participant's email"),
        ),
        migrations.AddField(
            model_name='registrationtraining',
            name='participant_hpno',
            field=models.CharField(blank=True, max_length=12, verbose_name="Participant's phone number"),
        ),
        migrations.AddField(
            model_name='registrationtraining',
            name='participant_icno',
            field=models.CharField(blank=True, max_length=12, verbose_name="Participant's IC number"),
        ),
        migrations.AddField(
            model_name='registrationtraining',
            name='participant_name',
            field=models.CharField(blank=True, max_length=50, verbose_name="Participant's name"),
        ),
        migrations.AddField(
            model_name='registrationtraining',
            name='payment_mode',
            field=models.CharField(choices=[('on', 'On'), ('off', 'Off')], max_length=5, null=True),
        ),
        migrations.AddField(
            model_name='registrationtraining',
            name='reviewed_by',
            field=models.CharField(blank=True, max_length=12),
        ),
        migrations.AddField(
            model_name='registrationtraining',
            name='training_type',
            field=models.CharField(choices=[('module1', 'Module 1'), ('module2', 'Module 2'), ('exam_practical_test', 'Exam Practical Test')], max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='training',
            name='created_by',
            field=models.CharField(max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='training',
            name='modified_by',
            field=models.CharField(max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='training',
            name='publish',
            field=models.CharField(choices=[('publish', 'Publish'), ('not_publish', 'Do Not Publish')], max_length=30, null=True),
        ),
        migrations.AddField(
            model_name='training',
            name='training_type',
            field=models.CharField(choices=[('module1', 'Module 1'), ('module2', 'Module 2'), ('exam', 'Exam'), ('practical', 'Practical'), ('test', 'Test')], max_length=30, null=True),
        ),
        migrations.AlterField(
            model_name='registrationtraining',
            name='registration_type',
            field=models.CharField(choices=[('individual', 'Individual'), ('group', 'Group')], max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='training',
            name='address1',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='training',
            name='address2',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='training',
            name='ccd_point',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='training',
            name='cert_type',
            field=models.CharField(choices=[('attendance', 'Attendance'), ('pass', 'Pass')], max_length=30, null=True, verbose_name='Certificate type'),
        ),
        migrations.AlterField(
            model_name='training',
            name='city',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='training',
            name='coach',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='training',
            name='from_date',
            field=models.DateTimeField(null=True, verbose_name='Date start'),
        ),
        migrations.AlterField(
            model_name='training',
            name='passing_mark',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='training',
            name='postcode',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='training',
            name='size',
            field=models.IntegerField(null=True, verbose_name='Size of the class'),
        ),
        migrations.AlterField(
            model_name='training',
            name='state',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='training',
            name='to_date',
            field=models.DateTimeField(null=True, verbose_name='Date end'),
        ),
    ]
