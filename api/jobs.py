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
    due_date = datetime.datetime.now() + datetime.timedelta(days=14)
    expired_payments = Payment.objects.all().filter(
        Q(created_date__lt=due_date,payment_status="0")|
        Q(created_date__lt=due_date,payment_status="-1")
    )
    for payment in expired_payments:
        cancel_proforma(payment.order_id)
        payment.proforma_cancelled="2"
        payment.save()