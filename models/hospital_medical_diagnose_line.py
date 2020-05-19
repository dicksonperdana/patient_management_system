from odoo import api, fields, models, _
from datetime import date,datetime

class medical_dianose_line(models.Model):
    _name ="medical.diagnose.line"

    doctor_assessment_id = fields.Many2one('outpatient.doctor.record')
    medical_record_id = fields.Many2one('outpatient.record', related='doctor_assessment_id.medical_record_id', string='Medical Record')
    diagnose_icd10 = fields.Many2one('hospital.icd10', string='ICD-10')
    description_icd10 = fields.Text(string='Deskripsi', related='diagnose_icd10.description')
    type_service_icd10 = fields.Selection([('0', 'Primary'), ('1', 'Secondary')], default="", string='Level')