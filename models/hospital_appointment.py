from odoo import models, api, fields, _
from odoo.exceptions import ValidationError
from datetime import date, datetime, timedelta
from dateutil.relativedelta import relativedelta

class HospitalAppointment(models.Model):

    _name = "hospital.appointment"
    _rec_name = 'appointment_id'
    _inherit = ['mail.thread', 'ir.needaction_mixin']


    def action_confirm(self):
        for rec in self:
            rec.state = 'confirm'


    def action_done(self):
        for rec in self:
            rec.state = 'done'


    def action_cancel(self):
        for rec in self:
            rec.state = 'cancel'


    @api.onchange('clinic')
    def onchange_clnic(self):
        b = {}
        if self.clinic:
            x_clinic = self.clinic.name
            b = {'domain':{'doctor_id': [('department_id','=', x_clinic)]}}
        return b


    def test_user_id(self):
        res = self.env['ir.config_parameter'].sudo().get_param('patient_management_system.path_clinic')
        raise ValidationError(res)


    @api.multi
    def open_medical_record(self):
        view_id = self.env.ref('patient_management_system.outpatient_record_form')
        return {
            'name': _('Outpatient Medical Record'),
            'res_model': 'outpatient.record',
            'view_id': view_id.id,
            'views': [(view_id.id, 'form')],
            'view_type': 'form',
            'view_mode': 'form',
            'type': 'ir.actions.act_window',
            'context': "{'default_patient_id': %d ,'default_appointment_ids': %d, 'default_clinic': %d }" % (self.patient_id.id, self.id, self.clinic.id)
        }

    @api.onchange('patient_id')
    def clinic_parent(self):
        path_clinic = self.env['ir.config_parameter'].sudo().get_param('patient_management_system.path_clinic_name')
        return {'domain': {'clinic': [('parent_id', '=', path_clinic)]}}

    @api.constrains('appointment_date_start','appointment_date_end')
    def check_date_appointment(self):
        data = self.env['hospital.appointment'].search_count([
                    ('appointment_date_start', '<', self.appointment_date_start),
                    ('appointment_date_end', '>', self.appointment_date_end),
                    ('doctor_id', '=', self.doctor_id.id)
                ])
        if data > 1:
            raise ValidationError("Time already booked")

    @api.multi
    def print_report(self):
        self.ensure_one()
        self.sent = True
        return self.env['report'].get_action(self, 'patient_management_system.report_appointment_card')

    appointment_id = fields.Char(string="AP", required=True, copy=False, readonly=True,
                                 index=True,default=lambda self: _('New'))
    patient_id = fields.Many2one('patient.record', string='Patient', required=True)
    no_rm = fields.Char(string='No. RM', related="patient_id.no_rm")
    patient_age = fields.Char(string='Umur', related="patient_id.patient_age")
    clinic = fields.Many2one('hr.department', string ="Klinik Tujuan")
    notes = fields.Text(string='Keterangan')
    appointment_date_registration = fields.Datetime(string='Tanggal Pendaftaran', required=True)
    appointment_date_start = fields.Datetime(string='Tanggal Kunjungan', required=True)
    appointment_date_end = fields.Datetime(string='Tanggal Kunjungan Akhir',required=True)
    doctor_id = fields.Many2one('hr.employee', required=True)
    is_medical_record = fields.Boolean(copy=False, default=False)

    @api.model
    def create(self, vals):
        if vals.get('appointment_id', _('New')) == _('New'):
            vals['appointment_id'] = self.env['ir.sequence'].next_by_code('appointment.record.sequence') or _('New')

        result = super(HospitalAppointment, self).create(vals)
        return result

    state = fields.Selection([
        ('draft', 'Unconfirmed'),
        ('confirm', 'Confirmed'),
        ('done', 'Done'),
        ('cancel', 'Cancelled')],
        string='Status', default='draft', readonly=True)
