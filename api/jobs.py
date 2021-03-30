from assessments.models import SampleResult, SyncResult
import shutil
import os

from app.helpers.docx2pdf import TEMPLATE_TEMP_PATH
def job_remove_temp():
    print("Cron: Remove Temp files")
    if os.path.exists(TEMPLATE_TEMP_PATH):
        shutil.rmtree(TEMPLATE_TEMP_PATH) 
        print('JOB: Clear up tmp folder')

from billings.models import Payment
from api.soap.create_transaction import cancel_proforma
import datetime
from django.utils.timezone import localtime, now
from django.db.models import Q

def job_cancel_proforma():
    print("Cron: Cancel Proforma")
    due_date = localtime(now()) - datetime.timedelta(days=14)
    expired_payments = Payment.objects.all().filter(
        Q(created_date__lt=due_date,payment_status="0",proforma_cancelled=False)|
        Q(created_date__lt=due_date,payment_status="-1",proforma_cancelled=False)
    )
    for payment in expired_payments:
        status = cancel_proforma(payment.order_id)
        if status.TransactionResult == "PASS":
            payment.proforma_cancelled=True
            payment.save()

def job_remove_failed_sync():
    print("Cron: Delete Failed Sync Result")
    sync_results = SyncResult.objects.all().filter(sync_complete=False)
    if len(sync_results) > 0:
        sync_results.delete()