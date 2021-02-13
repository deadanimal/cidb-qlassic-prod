from billings.models import ClaimApplication
from django.contrib import admin

from .models import ClaimApplication, Payment

# Register your models here.
admin.site.register(ClaimApplication)
admin.site.register(Payment)