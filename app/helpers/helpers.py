import io, os
from docxtpl import DocxTemplate
from app.helpers.docx2pdf import StreamingConvertedPdf, ConvertFileModelField
from django.conf import settings
import absoluteuri

def docx_to_pdf_stream(letter_template, context):
    response = docx_to_pdf_process_stream(letter_template, context, False)
    return response

def docx_to_pdf_download(letter_template, context):
    response = docx_to_pdf_process_stream(letter_template, context, True)
    return response

def docx_to_pdf_process_stream(letter_template, context, download):
    # Method 1
    # base_url = settings.MEDIA_ROOT + '/'
    # template_path = base_url + letter_template.template_file.name

    # Method 2
    # template_path = os.path.abspath(letter_template.template_file.url)
    
    # Method 5
    # template_path = requests.get(absoluteuri.build_absolute_uri(letter_template.template_file.url))

    template_path = os.path.join(settings.BASE_DIR,settings.MEDIA_ROOT,letter_template.template_file.name)
    print(template_path)
    # Method 3
    # template_path = absoluteuri.build_absolute_uri(letter_template.template_file.url)
    
    # Method 4
    # template_path = settings.MEDIA_ROOT + letter_template.template_file.name
    fileName, fileExtension = os.path.splitext(letter_template.template_file.name)

    doc = DocxTemplate(template_path)
    print(template_path)
    doc.render(context)
    # ... your other code ...
    doc_io = io.BytesIO() # create a file-like object
    doc.save(doc_io) # save data to file-like object
    doc_io.seek(0) # go to the beginning of the file-like object
    doc_io.name = letter_template.title + fileExtension
    doc_io.content_type = "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
    # response = HttpResponse(doc_io.read())

    # # Content-Disposition header makes a file downloadable
    # response["Content-Disposition"] = "attachment; filename=generated_doc.docx"

    # # Set the appropriate Content-Type for docx file
    # response["Content-Type"] = "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
    
    inst = StreamingConvertedPdf(doc_io, download=download)

    return inst.stream_content()

def docx_to_pdf_file(letter_template, context, qr_url):
    response = docx_to_pdf_process_file(letter_template, context, True, qr_url)
    return response

def docx_to_pdf_process_file(letter_template, context, download, qr_url):
    template_path = letter_template.template_file.path
    fileName, fileExtension = os.path.splitext(letter_template.template_file.name)
    doc = DocxTemplate(template_path)
    doc.render(context)
    if qr_url != None:
        doc.replace_pic('qr.png',qr_url)
    # ... your other code ...
    doc_io = io.BytesIO() # create a file-like object
    doc.save(doc_io) # save data to file-like object
    doc_io.seek(0) # go to the beginning of the file-like object
    doc_io.name = letter_template.title + fileExtension
    doc_io.content_type = "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
    # response = HttpResponse(doc_io.read())

    # # Content-Disposition header makes a file downloadable
    # response["Content-Disposition"] = "attachment; filename=generated_doc.docx"

    # # Set the appropriate Content-Type for docx file
    # response["Content-Type"] = "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
    inst = StreamingConvertedPdf(doc_io, download=download)

    return inst.file_content()

    
