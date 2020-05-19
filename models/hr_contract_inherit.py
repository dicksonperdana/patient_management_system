from odoo import api, fields, models, _
from odoo.exceptions import ValidationError

class payslipsInherit(models.Model):
    _inherit = 'hr.contract'

    def test_button(self):
        account_invoice_report = self.env['account.invoice.report']

        where_query = account_invoice_report._where_calc([
            ('state', '=', 'paid'),
            ('user_id', '=', self.employee_id.user_id.id),
            ('date_due', '>=', self.date_start),
            ('date_due', '<=', self.date_end),
            ('type', '=', 'out_invoice')
        ])

        account_invoice_report._apply_ir_rules(where_query, 'read')
        from_clause, where_clause, where_clause_params = where_query.get_sql()
        query = """
                              SELECT SUM(price_total) as total, partner_id
                                FROM account_invoice_report account_invoice_report
                               WHERE %s
                               GROUP BY partner_id
                            """ % where_clause

        self.env.cr.execute(query, where_clause_params)
        price_totals = self.env.cr.dictfetchall()
        # raise ValidationError(a)
        self.wage = sum(price['total'] for price in price_totals)


