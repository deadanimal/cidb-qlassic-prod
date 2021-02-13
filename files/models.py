# from django.db import models
# import uuid
# from trainings.models import JoinedTraining, ApplicationTrainer
# from assessments.models import QlassicAssessmentApplication

# from core.helpers import PathAndRename
# # Create your models here.

# class File(models.Model):
#     id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
#     jt = models.ForeignKey(JoinedTraining, on_delete=models.CASCADE, blank=True)
#     qaa = models.ForeignKey(QlassicAssessmentApplication, on_delete=models.CASCADE, blank=True)
#     at = models.ForeignKey(ApplicationTrainer, on_delete=models.CASCADE, blank=True)

#     upload = models.FileField(null=True, upload_to=PathAndRename('documents'))
#     name = models.CharField(max_length=255)
    
#     # Date
#     created_date = models.DateTimeField(auto_now_add=True)
#     modified_date = models.DateTimeField(auto_now=True)

#     def __str__(self):
#         return self.qaa