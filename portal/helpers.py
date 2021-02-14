from django.contrib import messages

# Models


TEMPLATE_TYPE = [
    # To follow SRS
    ('qlassic_score_letter','QLASSIC Score letter'),
    ('qlassic_certificate','QLASSIC Certificate'),
    ('qlassic_report','QLASSIC Report'),
    ('training_certificate','Training Certificate'),
    ('trainer_interview_letter','Trainer Interview Letter'),
    ('qca_interview_letter','QCA Interview Letter'),
    ('trainer_reject_letter','Trainer Rejection Letter'),
    ('qca_reject_letter','QCA Rejection Letter'),
    ('attendance_sheet','Attendance Sheet'),
    ('accreditation_letter','Accreditation Letter'),
    ('accreditation_certificate','Accreditation Certificate'),
]