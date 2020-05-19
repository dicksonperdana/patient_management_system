from odoo import models, fields, api, _
from odoo.exceptions import ValidationError

class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    @api.model
    def default_get(self, fields):
        res = super(ResConfigSettings, self).default_get(fields)
        clinic_path = self.env['ir.config_parameter'].sudo().get_param('patient_management_system.path_clinic')
        res.update(
            path_clinic=int(clinic_path)
        )
        return res

    @api.one
    def set_values(self):
        self.env['ir.config_parameter'].set_param('patient_management_system.path_clinic_name', self.path_clinic.name)
        self.env['ir.config_parameter'].set_param('patient_management_system.path_clinic', self.path_clinic.id)


    path_clinic = fields.Many2one('hr.department', string="Clinic Path")





