from odoo import models, fields, api, _


class res_partner(models.Model):
    _inherit = 'res.partner'

    patient = fields.Boolean(string='Patient')
    person = fields.Boolean(string="Person")

    @api.multi
    def action_see_attachments_perjanjian(self):
        domain = [('res_model', '=', 'res.partner'), ('res_id', '=', self.id)]
        attachment_view = self.env.ref('patient_management_system.view_document_file_kanban_outpatient')
        return {
            'name': _('Attachments'),
            'domain': domain,
            'res_model': 'ir.attachment',
            'type': 'ir.actions.act_window',
            'view_id': attachment_view.id,
            'views': [(attachment_view.id, 'kanban'), (False, 'form')],
            'view_mode': 'kanban,tree,form',
            'view_type': 'form',
            'help': _('''<p class="oe_view_nocontent_create">
                        Click to upload files to your product.
                    </p><p>
                        Use this feature to store any files, like drawings or specifications.
                    </p>'''),
            'limit': 80,
            'context': "{'default_res_model': '%s','default_res_id': %d}" % ('res.partner', self.id)
        }