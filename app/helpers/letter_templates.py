
from django.contrib import messages
from portal.models import LetterTemplate
from app.helpers.helpers import docx_to_pdf_download, docx_to_pdf_stream
from core.helpers import translate_malay_date
import datetime

def test_letter_template(id, template_type):
    if template_type == 'interview_letter':
        response = test_template_interview_letter(id)
        return response


def test_template_interview_letter(id):
    letter_template = LetterTemplate.objects.get(id=id)
    context = {
        'invitation': {
            'iv_date': translate_malay_date(datetime.date.today().strftime("%d %B %Y")),
            'iv_from_time': '11:00am',
            'iv_to_time': '12:00pm',
            'iv_session': 'Tengah Hari',
            'iv_location': 'Bilik 1, Tingkat 33, CIDB, Kuala Lumpur'
        }
    }
    response = docx_to_pdf_stream(letter_template, context)
    return response

# Actual Value
def generate_document(request, template_type, context):
    letter_templates = LetterTemplate.objects.all().filter(template_type=template_type,is_active=True).order_by('-modified_date')
    lt = None
    if len(letter_templates) > 0:
        lt = letter_templates[0]
    else:
        messages.warning(request,'Letter template not found. Please insert the letter template and set it to active to generate the document.')
        return None
    
    response = docx_to_pdf_stream(lt, context)
    return response