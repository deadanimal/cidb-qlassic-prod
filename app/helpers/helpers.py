import io
from docxtpl import DocxTemplate
from app.helpers.docx2pdf import StreamingConvertedPdf

def docx_to_pdf_stream(letter_template, context):
    response = docx_to_pdf_process(letter_template, context, False)
    return response

def docx_to_pdf_download(letter_template, context):
    response = docx_to_pdf_process(letter_template, context, True)
    return response

def docx_to_pdf_process(letter_template, context, download):
    template_path = letter_template.template_file.path
    doc = DocxTemplate(template_path)
    print(template_path)
    doc.render(context)
    # ... your other code ...
    doc_io = io.BytesIO() # create a file-like object
    doc.save(doc_io) # save data to file-like object
    doc_io.seek(0) # go to the beginning of the file-like object
    doc_io.name = letter_template.title + '.docx'
    doc_io.content_type = "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
    # response = HttpResponse(doc_io.read())

    # # Content-Disposition header makes a file downloadable
    # response["Content-Disposition"] = "attachment; filename=generated_doc.docx"

    # # Set the appropriate Content-Type for docx file
    # response["Content-Type"] = "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
    
    inst = StreamingConvertedPdf(doc_io, download=download)

    return inst.stream_content()