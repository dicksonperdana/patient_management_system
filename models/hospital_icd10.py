from odoo import models, api, fields, _
# from datetime import date, datetime
# from dateutil.relativedelta import relativedelta


class disease_icd10(models.Model):
    _name = "hospital.icd10"
    _rec_name = "icd10_dx_id"
    _inherit = ['mail.thread', 'ir.needaction_mixin']

    icd10_dx_id = fields.Char(string="Kode", required=True)
    description = fields.Text(string="Deskripsi", required=True)