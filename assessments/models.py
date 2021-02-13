from django.db import models
import uuid

# Models
from trainings.models import JoinedTraining, RoleApplication
from users.models import CustomUser, Assessor
from projects.models import ProjectInfo
# from projects.models import ProjectInfo

# Helper
from core.helpers import PathAndRename, STATE_CHOICES

# Signals
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.
class QlassicAssessmentApplication(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True)
    qaa_number = models.CharField(null=True, max_length=50, verbose_name="QLASSIC Assessment Application Number")
    pi = models.ForeignKey(ProjectInfo, on_delete=models.CASCADE, null=True)
    # sd = models.ForeignKey(SupportingDocuments, on_delete=models.CASCADE, null=True)
    # contractor = models.ForeignKey('projects.Contractor', on_delete=models.CASCADE, null=True)

    applicant_name = models.CharField(null=True, max_length=255)
    
    ROLE_CHOICES = [
        # To follow SRS
        ('superadmin','Super Admin'),
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
    
    organization = models.TextField(null=True, max_length=255)
    designation = models.CharField(null=True, max_length=255)
    address1 = models.CharField(null=True, max_length=255, verbose_name="Address 1")
    address2 = models.CharField(null=True, max_length=255, verbose_name="Address 2")
    postcode = models.CharField(null=True, max_length=10, verbose_name='Postal code')
    city = models.CharField(null=True, max_length=50)
    state = models.CharField(choices=STATE_CHOICES, null=True, max_length=50)    

    hp_no = models.CharField(null=True, max_length=15, verbose_name='Contact number')
    fax_no = models.CharField(null=True, max_length=15, verbose_name='Fax number')
    email = models.CharField(null=True, max_length=255)
    
    CONTRACT_TYPE = [
        # To follow SRS
        ('lump_sum','Lump Sum'),
        ('provisional_quantity','Provisional Quantity'),
        ('lum_sump_and_quantity','Lump Sum and Quantity'),
    ]

    contract_type = models.CharField(
        null=True,
        choices=CONTRACT_TYPE,
        max_length=50
    )

    BUILDING_TYPE = [
        # To follow SRS
        ('A','A - Landed Housing'),
        ('B','B - Stratified Housing'),
        ('C','C - Public/ Commercial/ Industrial Building (Without centralized cooling system)'),
        ('D','D - Public/ Commercial/ Industrial Building (With centralized cooling system)'),
    ]
    building_type = models.CharField(
        null=True,
        choices=BUILDING_TYPE,
        max_length=50
    )
    
    project_declaration_number = models.CharField(null=True, max_length=50)
    
    APPLICATION_STATUS = [
        # To follow SRS
        ('pending','Pending'),
        ('reviewed','Reviewed'),
        ('verified','Verified'),
        ('rejected','Rejected'),
        ('rejected_amendment','Rejected (With Amendment)'),
        ('need_payment','Need Payment'),
        ('paid','Paid'),
        ('assessor_assign','Assessor Assign'),
        ('confirm','Confirm'),
        ('in_progress','In-Progress'),
        ('completed','Completed'),
        ('approved','Approved'),
    ]
    application_status = models.CharField(
        null=True,
        blank=True,
        choices=APPLICATION_STATUS,
        max_length=50
    )

    proposed_date = models.DateField(null=True, verbose_name='Proposed date for assessment')
    assessment_date = models.DateField(null=True, verbose_name="Assessment date")

    NO_OF_ASSESSOR = [
        # To follow SRS
        (2,'2'),
        (4,'4'),
        (6,'6'),
        (8,'8'),
        (10,'10'),
    ]
    no_of_assessor = models.IntegerField(
        null=True,
        choices=NO_OF_ASSESSOR,
        verbose_name="Number of assessor",
    )

    no_of_blocks = models.IntegerField(null=True, verbose_name="Number of block/zone/assessment")

    PAYMENT_MODE = [
        # To follow SRS
        ('on','On'),
        ('off','Off'),
    ]
    payment_mode = models.CharField(
        null=True,
        choices=PAYMENT_MODE,
        max_length=5
    )

    qlassic_score = models.FloatField(null=True,blank=True, verbose_name='QLASSIC Score')

    reviewed_by = models.CharField(null=True, max_length=50)
    reviewed_date = models.DateTimeField(null=True)
    remarks1 = models.TextField(null=True, blank=True, max_length=255, verbose_name="Remarks 1 - by CASC Reviewer")
    verified_by = models.CharField(null=True, max_length=50)
    verified_date = models.DateTimeField(null=True)
    remarks2 = models.TextField(null=True, blank=True, max_length=255, verbose_name="Remarks 2 - by CASC Verifier")
    # approved_by = models.CharField(null=True, max_length=50)
    # approved_date = models.DateTimeField(null=True)
    # remarks3 = models.TextField(null=True, blank=True, max_length=255)

    # Date
    created_date = models.DateTimeField(auto_now_add=True)
    created_by = models.CharField(null=True, max_length=50)
    modified_date = models.DateTimeField(auto_now=True)
    modified_by = models.CharField(null=True, max_length=50)
   
    def __str__(self):
        return "%s - %s" % (self.created_date, self.qaa_number)

class Component(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
    name = models.CharField(null=True, max_length=255)

    # Date
    created_date = models.DateTimeField(auto_now_add=True)
    created_by = models.CharField(null=True, max_length=50)
    modified_date = models.DateTimeField(auto_now=True)
    modified_by = models.CharField(null=True, max_length=50)

    def __str__(self):
        return '%s' % (self.name)

class SubComponent(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
    name = models.CharField(null=True, max_length=255)
    
    component = models.ForeignKey(Component, on_delete=models.CASCADE, null=True)

    # Date
    created_date = models.DateTimeField(auto_now_add=True)
    created_by = models.CharField(null=True, max_length=50)
    modified_date = models.DateTimeField(auto_now=True)
    modified_by = models.CharField(null=True, max_length=50)

    def __str__(self):
        return '%s' % (self.name)

class Element(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    sub_component = models.ForeignKey(SubComponent, on_delete=models.CASCADE, null=True)
    name = models.CharField(null=True, max_length=255)

    # Date
    created_date = models.DateTimeField(auto_now_add=True)
    created_by = models.CharField(null=True, max_length=50)
    modified_date = models.DateTimeField(auto_now=True)
    modified_by = models.CharField(null=True, max_length=50)

    def __str__(self):
        return '%s (%s)' % (self.name, self.sub_component.name)

class DefectGroup(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    element = models.ForeignKey(Element, on_delete=models.CASCADE, null=True)
    
    name = models.CharField(null=True, max_length=255)
    
    NO_OF_CHECK = [
        # To follow SRS
        (1,'1'),
        (2,'2'),
        (3,'3'),
        (4,'4'),
        (5,'5'),
    ]
    no_of_check = models.IntegerField(
        null=True,
        choices=NO_OF_CHECK,
        verbose_name='Number of Check',
        default=1
    )
    
    # Date
    created_date = models.DateTimeField(auto_now_add=True)
    created_by = models.CharField(null=True, max_length=50)
    modified_date = models.DateTimeField(auto_now=True)
    modified_by = models.CharField(null=True, max_length=50)

    def __str__(self):
        return '%s (%s / %s)' % (self.name, self.element.sub_component.name, self.element.name)

class AssessmentData(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True)
    qaa = models.ForeignKey(QlassicAssessmentApplication, on_delete=models.CASCADE, null=True)
    assessor = models.ForeignKey(Assessor, on_delete=models.CASCADE, null=True)
    
    # sub_component = models.ForeignKey(SubComponent, on_delete=models.CASCADE, null=True)
    # dg = models.ForeignKey(DefectGroup, on_delete=models.CASCADE, null=True)
    
    block = models.IntegerField(null=True, verbose_name="Block's name")
    unit = models.IntegerField(null=True, verbose_name="Unit number")
    time = models.TimeField(null=True, verbose_name="Time taken to complete data for one sample")
    count_sampling_done = models.IntegerField(null=True, verbose_name="Number of sampling done")
    count_principle = models.IntegerField(null=True, verbose_name="Number of principles samples")
    count_services = models.IntegerField(null=True, verbose_name="Number of services samples")
    count_circulation = models.IntegerField(null=True, verbose_name="Number of circulation samples")
    
    number_of_sample = models.IntegerField(null=True)
    
    architectural_work = models.FloatField(null=True)
    floor_finishes = models.FloatField(null=True)
    internal_wall = models.FloatField(null=True)
    ceiling = models.FloatField(null=True)
    door = models.FloatField(null=True)
    window = models.FloatField(null=True)
    internal_fixtures = models.FloatField(null=True)
    roof = models.FloatField(null=True)
    external_wall = models.FloatField(null=True)
    apron_perimeter_drain = models.FloatField(null=True)
    car_park = models.FloatField(null=True, verbose_name="Car park/ Car porch")
    material_functional_test = models.FloatField(null=True, verbose_name="Material & Functional Test")
    
    total = models.FloatField(null=True, verbose_name="Total (1.1-5)")
    me_fittings = models.FloatField(null=True, verbose_name="Basic M&E Fittings")
    mock_up_score = models.FloatField(null=True, verbose_name="QLASSIC score with mock up")
    qlassic_score = models.FloatField(null=True, verbose_name="QLASSIC score")

    # Date
    created_date = models.DateTimeField(auto_now_add=True)
    created_by = models.CharField(null=True, max_length=50)
    modified_date = models.DateTimeField(auto_now=True)
    modified_by = models.CharField(null=True, max_length=50)

    def __str__(self):
        return str(self.qaa) if self.qaa else ''

class SupportingDocuments(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    jt = models.ForeignKey(JoinedTraining, on_delete=models.CASCADE, null=True, blank=True)
    ra = models.ForeignKey(RoleApplication, on_delete=models.CASCADE, null=True, blank=True)
    qaa = models.ForeignKey(QlassicAssessmentApplication, on_delete=models.CASCADE, null=True, blank=True)
    
    file_name = models.CharField(null=True, max_length=255)
    file = models.FileField(null=True, max_length=255, upload_to=PathAndRename('documents'))
    
    upload_date = models.DateTimeField(auto_now_add=True)

    # Date
    created_date = models.DateTimeField(auto_now_add=True)
    created_by = models.CharField(null=True, max_length=50)
    modified_date = models.DateTimeField(auto_now=True)
    modified_by = models.CharField(null=True, max_length=50)
   
    def __str__(self):
        return str(self.id)

class SuggestedAssessor(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    qaa = models.ForeignKey(QlassicAssessmentApplication, on_delete=models.CASCADE, null=True)
    assessor = models.ForeignKey(Assessor, on_delete=models.CASCADE, null=True)
    # pi = models.ForeignKey(ProjectInfo, on_delete=models.CASCADE, null=True)
    
    project_location = models.CharField(null=True, max_length=255)
    assessor_no = models.CharField(null=True, max_length=255, verbose_name="Assessor number")
    role_in_project = models.CharField(null=True, max_length=255)

    ACCEPTION = [
        # To follow SRS
        ('accept','Accept'),
        ('reject','Reject'),
    ]
    acception = models.CharField(
        null=True,
        choices=ACCEPTION,
        max_length=10
    )

    remarks = models.CharField(null=True, max_length=255)

    # Date
    created_date = models.DateTimeField(auto_now_add=True)
    created_by = models.CharField(null=True, max_length=50)
    modified_date = models.DateTimeField(auto_now=True)
    modified_by = models.CharField(null=True, max_length=50)
   
    def __str__(self):
        return self.assessor_no

class AssignedAssessor(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    assessor = models.ForeignKey(Assessor, on_delete=models.CASCADE, null=True)
    ad = models.ForeignKey(AssessmentData, on_delete=models.CASCADE, null=True)

    assessor_number = models.CharField(null=True, max_length=255)
    name = models.CharField(null=True, max_length=255)
    
    ROLE_IN_ASSESSMENT = [
        # To follow SRS
        ('lead_assessor','Lead Assessor'),
        ('assessor','Assessor'),
    ]
    role_in_assessment = models.CharField(
        null=True,
        choices=ROLE_IN_ASSESSMENT,
        max_length=30
    )

    # Date
    created_date = models.DateTimeField(auto_now_add=True)
    created_by = models.CharField(null=True, max_length=50)
    modified_date = models.DateTimeField(auto_now=True)
    modified_by = models.CharField(null=True, max_length=50)
   
    def __str__(self):
        return self.name

class WorkCompletionForm(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    qaa = models.ForeignKey(QlassicAssessmentApplication, on_delete=models.CASCADE, null=True)
    assessor = models.ForeignKey(Assessor, on_delete=models.CASCADE, null=True)
    assessor_number = models.CharField(null=True, max_length=255)
    # pi = models.ForeignKey(ProjectInfo, on_delete=models.CASCADE, null=True)
    ad = models.ForeignKey(AssessmentData, on_delete=models.CASCADE, null=True)

    name = models.CharField(null=True, max_length=255)
    icno = models.CharField(null=True, max_length=14, verbose_name="IC number")
    company = models.CharField(null=True, max_length=255)
    position = models.CharField(null=True, max_length=255)
    hp_no = models.CharField(null=True, max_length=255, verbose_name="Contact number")
    email = models.CharField(null=True, max_length=255)
    
    qaa_number = models.CharField(null=True, max_length=255, verbose_name="QLASSIC Assessment Application number")
    project_location = models.CharField(null=True, max_length=255)
    assessment_start_date = models.DateField(null=True, verbose_name='Assessment start date')
    assessment_end_date = models.DateField(null=True, verbose_name='Assessment end date')
    number_of_sample = models.IntegerField(null=True)
    number_of_form_used = models.IntegerField(null=True)

    # Date
    created_date = models.DateTimeField(auto_now_add=True)
    created_by = models.CharField(null=True, max_length=50)
    modified_date = models.DateTimeField(auto_now=True)
    modified_by = models.CharField(null=True, max_length=50)
   
    def __str__(self):
        return str(self.name)

class QlassicReporting(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    qaa = models.ForeignKey(QlassicAssessmentApplication, on_delete=models.CASCADE, null=True)
    qaa_number = models.CharField(null=True, max_length=255)
    # pi = models.ForeignKey(ProjectInfo, on_delete=models.CASCADE, null=True)
    ad = models.ForeignKey(AssessmentData, on_delete=models.CASCADE, null=True)

    report_number = models.CharField(null=True, max_length=255)
    
    TYPE_OF_REPORT = [
        # To follow SRS
        ('qlassic_score_letter','QLASSIC Score Letter'),
        ('qlassic_certificate','QLASSIC Certificate'),
        ('qlassic_report','QLASSIC Report'),
    ]
    type_of_report = models.CharField(
        null=True,
        choices=TYPE_OF_REPORT,
        max_length=30
    )
    
    # Date
    created_by = models.CharField(null=True, max_length=50)
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)
    modified_by = models.CharField(null=True, max_length=50)
   
    def __str__(self):
        return self.qaa

class SiteAttendance(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    qaa = models.ForeignKey(QlassicAssessmentApplication, on_delete=models.CASCADE, null=True)
    qaa_no = models.CharField(null=True, max_length=255, verbose_name="QLASSIC Assessment Application number")
    
    name = models.CharField(null=True, max_length=255)
    position = models.CharField(null=True, max_length=255)
    hp_no = models.CharField(null=True, max_length=255, verbose_name="Contact number")
    company = models.CharField(null=True, max_length=255)
    signature = models.CharField(null=True, max_length=255)
    
    assessment_date = models.DateField(null=True, verbose_name='Assessment date')
    
    def __str__(self):
        return self.qaa_no

class SubComponentResult(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    sub_component = models.ForeignKey(SubComponent, on_delete=models.CASCADE, null=True)
    assessment_data = models.ForeignKey(AssessmentData, on_delete=models.CASCADE, null=True)

    # Date
    created_date = models.DateTimeField(auto_now_add=True)
    created_by = models.CharField(null=True, max_length=50)
    modified_date = models.DateTimeField(auto_now=True)
    modified_by = models.CharField(null=True, max_length=50)

    def __str__(self):
        return '%s' % (self.assessment_data)

class SubComponentResultDocument(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    sub_component_result = models.ForeignKey(SubComponentResult, on_delete=models.CASCADE, null=True)
    file_name = models.CharField(null=True, max_length=255)
    file = models.FileField(null=True, max_length=255, upload_to=PathAndRename('results'))

    # Date
    created_date = models.DateTimeField(auto_now_add=True)
    created_by = models.CharField(null=True, max_length=50)
    modified_date = models.DateTimeField(auto_now=True)
    modified_by = models.CharField(null=True, max_length=50)
   
    def __str__(self):
        return self.file_name

class DefectGroupResult(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    defect_group = models.ForeignKey(DefectGroup, on_delete=models.CASCADE, null=True)
    assessment_data = models.ForeignKey(AssessmentData, on_delete=models.CASCADE, null=True)

    SCORE = [
        # To follow SRS
        (0,'Fail'),
        (1,'Pass'),
    ]
    score = models.IntegerField(
        null=True,
        default=0,
        choices=SCORE,
    )

    applicable = models.BooleanField(default=True)
    
    # Date
    created_date = models.DateTimeField(auto_now_add=True)
    created_by = models.CharField(null=True, max_length=50)
    modified_date = models.DateTimeField(auto_now=True)
    modified_by = models.CharField(null=True, max_length=50)

    def __str__(self):
        return '%s' % (self.assessment_data)