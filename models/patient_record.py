from ast import literal_eval
from operator import itemgetter
import time

from odoo import models, api, fields, _
from datetime import date, datetime
from dateutil.relativedelta import relativedelta
from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT
from odoo.exceptions import ValidationError
from odoo.addons.base.res.res_partner import WARNING_MESSAGE, WARNING_HELP


class PatientRecord(models.Model):
    _name = 'patient.record'
    _rec_name = 'patient_id'
    _inherit = ['mail.thread', 'ir.needaction_mixin']

    @api.depends('date_of_birth')
    def onchange_age(self):
        if self.date_of_birth:
            dt = self.date_of_birth
            d1 = datetime.strptime(dt, "%Y-%m-%d").date()
            d2 = datetime.today()
            rd = relativedelta(d2, d1)
            self.patient_age = str(rd.years) + "y" + " " + str(rd.months) + "m" + " " + str(rd.days) + "d"
        else:
            self.patient_age = "Date of Birth is Empty"

    @api.multi
    def open_patient_appointment(self):
        return {
            'name': _('Appointment'),
            'domain': [('patient_id', '=', self.id)],
            'view_type': 'form',
            'view_mode': 'tree,form',
            'res_model': 'hospital.appointment',
            'view_id': False,
            'type': 'ir.actions.act_window',
        }

    @api.multi
    def open_outpatient_record(self):
        return {
            'name': _('Outpatient'),
            'domain': [('patient_id', '=', self.id)],
            'view_type': 'form',
            'view_mode': 'tree,form',
            'res_model': 'outpatient.record',
            'view_id': False,
            'type': 'ir.actions.act_window',
        }

    @api.onchange('patient_id')
    def check_patient(self):
        res = self.search_count([('patient_id', '=', self.patient_id.id)])
        if res >= 1:
            raise ValidationError(_('User Already Exist'))

    @api.constrains('patient_id')
    def check_patient_constrains(self):
        res = self.search_count([('patient_id', '=', self.patient_id.id)])
        if res >= 1:
            raise ValidationError(_('User Already Exist'))

    def open_invoice_record(self):
        action = self.env.ref('account.action_invoice_refund_out_tree').read()[0]
        action['domain'] = literal_eval(action['domain'])
        action['domain'].append(('partner_id', 'child_of', self.patient_id.ids))
        return action

    def get_outpatient_record_count(self):
        count = self.env['outpatient.record'].search_count([('patient_id', '=', self.id)])
        self.outpatient_record_count = count

    def get_appointment_count(self):
        count = self.env['hospital.appointment'].search_count([('patient_id', '=', self.id)])
        self.appointment_count = count

    def check_user_currency(self):
        raise ValidationError(self.patient_id.company_id.currency_id.id)

    no_rm = fields.Char(string="No Rekam Medis", required=True, copy=False, readonly=True, index=True,
                        default=lambda self: _('New'))
    patient_id = fields.Many2one('res.partner', domain=[('patient', '=', True)], string='Nama', required=True)
    image = fields.Binary(string="Image")
    notes = fields.Text(string="Keterangan")
    sex = fields.Selection([('m', 'Laki-Laki'), ('f', 'Perempuan')], string="Jenis Kelamin")
    date_of_birth = fields.Date(string="Tanggal Lahir")
    patient_age = fields.Char(compute=onchange_age, string="Umur", store=True)
    religion = fields.Selection([('Islam', 'Islam'), ('Katolik', 'Katolik'), ('Kristen', 'Kristen'), ('Buddha', 'Buddha')
                                    , ('Konghucu', 'Kong Hu Cu')], string="Agama")
    rh = fields.Selection([('-+', '+'), ('--', '-')], string="Rh")
    patient_citizen_id = fields.Char(string='No KTP', required=True)
    birth_place = fields.Char(string='Tempat Lahir', required=True)
    marital = fields.Selection([('K', 'Kawin'), ('BK', 'Belum Kawin')], string='Status')
    mother_name = fields.Char(string='Nama Ibu Kandung')
    education = fields.Selection(
        [('TS', 'Tidak Sekolah'), ('SD', 'Sekolah Dasar'), ('SMP', 'Menengah Pertama'), ('SMA', 'Menengah Atas'),
         ('S1', 'Sarjana'), ('S2', 'Magister'), ('S3', 'Doktor')], string='pendidikan')
    nationality = fields.Selection([('WNI', 'Indonesia'), ('WNA', 'Asing')], string="Warga negara")
    phone = fields.Char(string="Handphone")
    rujukan = fields.Selection([('DS', 'Datang Sendiri'), ('RJ', 'Rujukan')], string="Rujukan")
    blood_type = fields.Selection([('A', 'A'), ('B', 'B'), ('AB', 'AB'), ('O', 'O')], string="Gol. Darah")
    country = fields.Char(string="Negara")
    provence = fields.Char(string="Provinsi")
    region = fields.Char(string="Kabupaten/Kota")
    district = fields.Char(string="Kecamatan")
    job_status = fields.Selection([('PNS', 'Pegawai Negeri'), ('SW', 'Swasta')], string="Pekerjaan")
    address = fields.Text(string="Alamat")
    appointment_count = fields.Integer(string="Appointment", compute='get_appointment_count')
    outpatient_record_count = fields.Integer(string="Outpatient Record", compute='get_outpatient_record_count')
    customer_invoice_count = fields.Integer(string="Customer Invoice", compute='get_invoice_count')
    total_invoiced = fields.Monetary(compute='_invoiced_total', string="Total Invoiced", groups='account.group_account_invoice')
    currency_id = fields.Many2one('res.currency', string='Currency')

    @api.model
    def create(self, vals):
        if vals.get('no_rm', _('New')) == _('New'):
            vals['no_rm'] = self.env['ir.sequence'].next_by_code('patient.record.sequence') or _('New')

        result = super(PatientRecord, self).create(vals)
        return result

    @api.multi
    def _invoiced_total(self):
        account_invoice_report = self.env['account.invoice.report']
        if not self.patient_id.ids:
            return True
        user_currency_id = self.env.user.company_id.currency_id.id
        all_partners_and_children = {}
        all_partner_ids = []
        for partner in self:
            # price_total is in the company currency
            all_partners_and_children[partner.patient_id] = self.env['res.partner'].with_context(active_test=False).search(
                [('id', 'child_of', partner.patient_id.id)]).ids
            all_partner_ids += all_partners_and_children[partner.patient_id]

        where_query = account_invoice_report._where_calc([
            ('partner_id', 'in', all_partner_ids), ('state', 'not in', ['draft', 'cancel']),
            ('type', 'in', ('out_invoice', 'out_refund'))
        ])
        account_invoice_report._apply_ir_rules(where_query, 'read')
        from_clause, where_clause, where_clause_params = where_query.get_sql()
        # price_total is in the company currency
        query = """
                      SELECT SUM(price_total) as total, partner_id
                        FROM account_invoice_report account_invoice_report
                       WHERE %s
                       GROUP BY partner_id
                    """ % where_clause
        self.env.cr.execute(query, where_clause_params)
        price_totals = self.env.cr.dictfetchall()
        for partner, child_ids in all_partners_and_children.items():
            self.total_invoiced = sum(price['total'] for price in price_totals if price['partner_id'] in child_ids)
