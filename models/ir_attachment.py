from odoo import fields, models


class IrAttachmentO(models.Model):
    _inherit = 'ir.attachment'
    _order = "priority desc, id desc"

    priority = fields.Selection([
        ('0', 'Normal'),
        ('1', 'Low'),
        ('2', 'High'),
        ('3', 'Very High')], string="Priority", help="Gives the sequence order when displaying a list of tasks.")