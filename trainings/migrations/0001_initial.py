# Generated by Django 2.2.10 on 2020-10-20 06:45

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ApplicationTrainer',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('status', models.CharField(blank=True, max_length=255)),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('modified_date', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='JoinedTraining',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('year', models.IntegerField(blank=True)),
                ('course', models.CharField(blank=True, max_length=255)),
                ('place', models.CharField(blank=True, max_length=255)),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('modified_date', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='RegistrationTraining',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('registration_type', models.CharField(blank=True, max_length=255)),
                ('participant', models.CharField(blank=True, max_length=255)),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('modified_date', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Training',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('type_training', models.CharField(blank=True, max_length=255)),
                ('size', models.IntegerField(blank=True)),
                ('ccd_point', models.IntegerField(blank=True)),
                ('from_date', models.DateTimeField(blank=True)),
                ('to_date', models.DateTimeField(blank=True)),
                ('passing_mark', models.IntegerField(blank=True)),
                ('cert_type', models.CharField(blank=True, max_length=255)),
                ('address1', models.CharField(blank=True, max_length=255)),
                ('address2', models.CharField(blank=True, max_length=255)),
                ('postcode', models.IntegerField(blank=True)),
                ('city', models.CharField(blank=True, max_length=255)),
                ('state', models.CharField(blank=True, max_length=255)),
                ('coach', models.CharField(blank=True, max_length=255)),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('modified_date', models.DateTimeField(auto_now=True)),
            ],
        ),
    ]
