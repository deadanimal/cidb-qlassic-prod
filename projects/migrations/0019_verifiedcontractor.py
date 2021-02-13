# Generated by Django 2.2.10 on 2020-12-07 09:53

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('projects', '0018_auto_20201201_0828'),
    ]

    operations = [
        migrations.CreateModel(
            name='VerifiedContractor',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ssm_number', models.CharField(max_length=255, null=True)),
                ('contractor_registration_number', models.CharField(max_length=255, null=True)),
                ('is_verified', models.BooleanField(default=False)),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('created_by', models.CharField(max_length=50, null=True)),
                ('modified_date', models.DateTimeField(auto_now=True)),
                ('modified_by', models.CharField(max_length=50, null=True)),
                ('user_id', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, unique=True)),
            ],
        ),
    ]
