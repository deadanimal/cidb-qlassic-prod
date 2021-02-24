import shutil
import os

from app.helpers.docx2pdf import TEMPLATE_TEMP_PATH
def job_remove_temp():
    if os.path.exists(TEMPLATE_TEMP_PATH):
        shutil.rmtree(TEMPLATE_TEMP_PATH) 
    print('JOB: Clear up tmp folder')