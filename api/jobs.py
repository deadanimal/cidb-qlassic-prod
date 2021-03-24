import shutil
import os

from app.helpers.docx2pdf import TEMPLATE_TEMP_PATH
def job_remove_temp():
    if os.path.exists(TEMPLATE_TEMP_PATH):
        shutil.rmtree(TEMPLATE_TEMP_PATH) 
        print('JOB: Clear up tmp folder')

from billings.models import Payment
from api.soap.create_transaction import cancel_proforma
import datetime
from django.db.models import Q

def job_cancel_proforma():
    due_date = datetime.datetime.now() - datetime.timedelta(days=14)
    expired_payments = Payment.objects.all().filter(
        Q(created_date__lt=due_date,payment_status="0",proforma_cancelled=False)|
        Q(created_date__lt=due_date,payment_status="-1",proforma_cancelled=False)
    )
    for payment in expired_payments:
        status = cancel_proforma(payment.order_id)
        if status.TransactionResult == "PASS":
            payment.proforma_cancelled=True
            payment.save()