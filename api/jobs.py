import shutil
from app.helpers.docx2pdf import TEMPLATE_TEMP_PATH
def job_remove_temp():
    shutil.rmtree(TEMPLATE_TEMP_PATH) 
    print('JOB: Clear up tmp folder')