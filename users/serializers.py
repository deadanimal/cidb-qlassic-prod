from datetime import datetime
from calendar import timegm
import json

from django.contrib.auth.forms import PasswordResetForm
from django.conf import settings
from django.utils.translation import gettext as _
from rest_framework import serializers
from django.utils.timezone import now
#from api.settings import AWS_S3_ENDPOINT_URL, AWS_STORAGE_BUCKET_NAME

from .models import (
    CustomUser,
    Assessor,
)

class CustomUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = CustomUser
        fields = (
            'name', 
            'email', 
            'created_date',
            'is_active'
        )
        read_only_fields = ('email', 'id')


class AssessorSerializer(serializers.ModelSerializer):

    class Meta:
        model = Assessor
        fields = (
            'user', 
            'assessor_no', 
            'created_date'
        )
        read_only_fields = ('email', 'id')

