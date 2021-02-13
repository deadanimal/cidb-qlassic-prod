from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import ugettext_lazy as _

from .managers import CustomUserManager
import uuid

# Helpers
from core.helpers import PathAndRename, STATE_CHOICES

# Create your models here.
class CustomUser(AbstractUser):
    username = None
    email = models.EmailField(_('email address'), max_length=30, unique=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    icno = models.CharField(null=True, max_length=14, verbose_name='Identity Card Number')
    name = models.CharField(null=True, max_length=100)

    GENDER = [
        # To follow SRS
        ('MALE', 'MALE'),
        ('FEMALE', 'FEMALE'), 
    ]

    gender = models.CharField(
        null=True,
        max_length=10,
        choices=GENDER,
    )  

    MARITAL_STATUS = [
        # To follow SRS
        ('SINGLE','SINGLE'),
        ('MARRIED','MARRIED'),
        ('DIVORCED','DIVORCED'), 
    ]

    marital_status = models.CharField(
        null=True,
        max_length=10,
        choices=MARITAL_STATUS,
    )      

    greencard_no = models.CharField(null=True, blank=True, max_length=16, verbose_name='Green card number')
    greencard_exp_date = models.DateField(null=True, blank=True, verbose_name='Green card\'s expired date')

    organization = models.TextField(null=True, max_length=50)
    position = models.CharField(null=True, max_length=50)
    
    ROLE_CHOICES = [
        # To follow SRS
        ('superadmin','Super Admin'),
        ('staff','Staff'),
        ('contractor','Contractor'),
        ('assessor','Assessor'),
        ('trainer','Trainer'),
        ('trainee','Trainee'),
        ('applicant','Applicant'),
        ('casc_reviewer','CASC Reviewer'),
        ('casc_verifier','CASC Verifier'),
        ('casc_approver','CASC Approver'),
        ('cidb_reviewer','CIDB Reviewer'),
        ('cidb_verifier','CIDB Verifier'),
        ('cidb_approver','CIDB Approver'),
    ]
    
    role = models.CharField(
        null=True,
        choices=ROLE_CHOICES,
        max_length=50
    )

    # Transportation Detail
    transport_model = models.CharField(null=True, blank=True, max_length=50, verbose_name='Transport Model')
    transport_cc = models.FloatField(null=True, blank=True, verbose_name='CC')
    transport_registration_number = models.CharField(null=True, blank=True, max_length=50, verbose_name='Transport Registration Number')

    # Home Address
    address1 = models.CharField(null=True, max_length=100)
    address2 = models.CharField(null=True, max_length=100)
    postcode = models.CharField(null=True, max_length=10, verbose_name='Postal code')
    city = models.CharField(null=True, max_length=50)
    state = models.CharField(choices=STATE_CHOICES, null=True, max_length=50)    
    
    # Office Address
    # office_address1 = models.CharField(null=True, max_length=100)
    # office_address2 = models.CharField(null=True, max_length=100)
    # office_postcode = models.IntegerField(null=True, verbose_name='Postal code')
    # office_city = models.CharField(null=True, max_length=20)
    # office_state = models.CharField(choices=STATE_CHOICES, null=True, max_length=20)    

    # Phone
    office_no = models.CharField(null=True, max_length=15, verbose_name='Office phone number')
    hp_no = models.CharField(null=True, max_length=15, verbose_name='Mobile number')
    fax_no = models.CharField(null=True, max_length=15, verbose_name='Fax number')
    
    picture = models.FileField(null=True, blank=True, upload_to=PathAndRename('images'), verbose_name='Profile picture')
    
    # Date
    created_date = models.DateTimeField(auto_now_add=True)
    created_by = models.CharField(null=True, max_length=50)
    modified_date = models.DateTimeField(auto_now=True)
    modified_by = models.CharField(null=True, max_length=50)
   
    def __str__(self):
        return self.email


# @receiver(post_save, sender=SubComponent)
# def signal_sub_component(sender, instance, created, **kwargs):
#     if instance.
    # if created:
    #     instance.created_by = 
    # else:
    #     instance.profile.referral_code = 'NXU' + str(instance.profile.id) 
    # instance.save()

class AcademicQualification(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True)
    
    year = models.IntegerField(null=True, verbose_name="Graduation year")
    institution = models.CharField(null=True, max_length=50, verbose_name="Name of institution")
    
    QUALIFICATION = [
        # To follow SRS
        ('spm', 'SPM'),
        ('diploma', 'Diploma'), 
        ('degree', 'Degree'), 
        ('master', 'Master'), 
        ('phd', 'PHD'), 
    ]
    qualification = models.CharField(
        null=True,
        max_length=50,
        choices=QUALIFICATION,
    )  

    program = models.CharField(null=True, max_length=50, verbose_name="Academic program")

    # Date
    created_by = models.CharField(null=True, max_length=50)
    created_date = models.DateTimeField(auto_now_add=True)
    modified_by = models.CharField(null=True, max_length=50)
    modified_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user

class WorkExperience(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True)
    
    year_from = models.IntegerField(null=True, verbose_name="Year start")
    year_to = models.IntegerField(null=True, verbose_name="Year end")
    position = models.CharField(null=True, max_length=50)
    company = models.CharField(null=True, max_length=50)

    # Date
    created_by = models.CharField(null=True, max_length=50)
    created_date = models.DateTimeField(auto_now_add=True)
    modified_by = models.CharField(null=True, max_length=50)
    modified_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user

class Assessor(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(CustomUser, unique=True, on_delete=models.CASCADE, null=True)
    assessor_no = models.CharField(null=True, max_length=50, verbose_name='Assessor number')
    
    ASSESSOR_TYPE = [
        # To follow SRS
        ('QIA', 'QLASSIC Industry Assessor'),
        ('QCA', 'QLASSIC CIDB Assessor'),
    ]
    assessor_type = models.CharField(
        default='QIA',
        null=True,
        max_length=50,
        choices=ASSESSOR_TYPE,
    )  

    # Date
    created_by = models.CharField(null=True, max_length=50)
    created_date = models.DateTimeField(auto_now_add=True)
    modified_by = models.CharField(null=True, max_length=50)
    modified_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.assessor_no

class Trainer(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True)
    trainer_no = models.CharField(null=True, max_length=6, verbose_name='Trainer number')

    # Date
    created_by = models.CharField(null=True, max_length=50)
    created_date = models.DateTimeField(auto_now_add=True)
    modified_by = models.CharField(null=True, max_length=50)
    modified_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user