from ast import literal_eval
from operator import itemgetter
import time

from odoo import models, api, fields, _

class HospitalCashier(models.Model):
    _name = 'hospital.cashier'

    def open_invoice(self):
        action = self.env.ref('account.action_invoice_refund_out_tree').read()[0]
        action['domain'] = literal_eval(action['domain'])
        # action['domain'].append(('state', 'not in', ['paid']))
        action['domain'] = [('type','in', ['out_invoice']), ('comment','=','Invoice Created from Medical Service'),
                            ('state', 'not in', ['paid', 'cancel'])]
        return action

    def open_invoice_history(self):
        action = self.env.ref('account.action_invoice_refund_out_tree').read()[0]
        action['domain'] = literal_eval(action['domain'])
        # action['domain'].append(('state', 'not in', ['paid']))
        action['domain'] = [('type', 'in', ['out_invoice']), ('comment', '=', 'Invoice Created from Medical Service'),
                            ('state', 'not in', ['open'])]
        return action