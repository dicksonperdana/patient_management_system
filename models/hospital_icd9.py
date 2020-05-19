from odoo import models, api, fields, _
# from datetime import date, datetime
# from dateutil.relativedelta import relativedelta


class procedure_icd9(models.Model):
    _name = 'hospital.icd9'
    _rec_name = 'icd9_id'
    _inherit = ['mail.thread', 'ir.needaction_mixin']

    icd9_id = fields.Many2one('product.product', string="Kode", domain=[('type','=','service')], required=True)
    description = fields.Text(string='Deskripsi')
