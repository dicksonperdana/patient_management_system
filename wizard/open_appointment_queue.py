from ast import literal_eval
from odoo import api, fields, models, _
from datetime import date,datetime
from odoo.exceptions import Warning, UserError


class open_appointment_queue(models.TransientModel):
    _name = 'open.appointment.queue'

    @api.onchange('clinic_transient')
    def clinic_parent(self):
        path_clinic = self.env['ir.config_parameter'].sudo().get_param('patient_management_system.path_clinic_name')
        return {'domain': {'clinic_transient': [('parent_id', '=', path_clinic)]}}

    @api.onchange('clinic_transient')
    def onchange_clnic(self):
        b = {}
        if self.clinic_transient:
            x_clinic = self.clinic_transient.name
            b = {'domain':{'doctor_id_transient': [('department_id','=', x_clinic)]}}
        return b

    clinic_transient = fields.Many2one('hr.department', string="Klinik Tujuan")
    doctor_id_transient = fields.Many2one('hr.employee', required=True)

    def open_invoice_history(self):
        action = self.env.ref('patient_management_system.action_appointment_queue_nurse').read()[0]
        action['domain'] = literal_eval(action['domain'])
        action['domain'] = [('doctor_id','=', self.doctor_id_transient.id)]
        return action