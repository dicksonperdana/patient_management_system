from odoo import api, fields, models, _
from datetime import date,datetime

class medical_service_line(models.Model):
    _name ="medical.service.line"

    doctor_assessment_id = fields.Many2one('outpatient.doctor.record')
    medical_record_id = fields.Many2one('outpatient.record', related='doctor_assessment_id.medical_record_id', string='Medical Record')
    service_icd9 = fields.Many2one('hospital.icd9', string='ICD-9-CM')
    description_icd9 = fields.Text(string='Deskripsi', related='service_icd9.description')
    type_service_icd9 = fields.Selection([('0','Primary'),('1','Secondary')], default="", string='Level')