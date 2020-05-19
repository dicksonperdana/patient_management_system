# -*- coding: utf-8 -*-
# Part of BrowseInfo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _
from datetime import date,datetime
from odoo.exceptions import Warning, UserError


class create_medical_service_invoice(models.TransientModel):
    _name = 'create.service.invoice'

    @api.multi
    def create_service_invoice(self):
        active_ids = self._context.get('active_ids')
        active_ids = active_ids or False
        lab_req_obj = self.env['outpatient.record']
        account_invoice_obj = self.env['account.invoice']
        account_invoice_line_obj = self.env['account.invoice.line']
        ir_property_obj = self.env['ir.property']
        inv_list = []
        lab_reqs = lab_req_obj.browse(active_ids)
        for lab_req in lab_reqs:
            if len(lab_req.doctor_assessment_line.medical_service_line_ids) < 1 or lab_req.appointment_ids == 0:
                raise Warning('Invoice Cannot Be Created.')

            if lab_req.is_invoiced == True:
                raise Warning('All ready Invoiced.')
            sale_journals = self.env['account.journal'].search([('type', '=', 'sale')])
            invoice_vals = {
                'name': "Tagihan Pasien atas Nama %s " % (lab_req.patient_id.patient_id.name),
                'origin': lab_req.mr_id or '',
                'type': 'out_invoice',
                'reference': False,
                'partner_id': lab_req.doctor_assessment_line.patient_id.patient_id.id,
                'date_invoice': date.today(),
                'account_id': lab_req.doctor_assessment_line.patient_id.patient_id.property_account_receivable_id.id,
                'journal_id': sale_journals and sale_journals[0].id or False,
                'partner_shipping_id': lab_req.doctor_assessment_line.patient_id.patient_id.id,
                'currency_id': lab_req.doctor_assessment_line.patient_id.patient_id.currency_id.id,
                'payment_term_id': False,
                'fiscal_position_id': lab_req.doctor_assessment_line.patient_id.patient_id.property_account_position_id.id,
                'team_id': False,
                'comment': "Invoice Created from Medical Service",
                'company_id': lab_req.doctor_assessment_line.patient_id.patient_id.company_id.id or False,
                'state': 'draft',
            }

            res = account_invoice_obj.create(invoice_vals)
            for p_line in lab_req.doctor_assessment_line.medical_service_line_ids:

                invoice_line_account_id = False
                if p_line.service_icd9.icd9_id.id:
                    invoice_line_account_id = p_line.service_icd9.icd9_id.property_account_income_id.id or p_line.service_icd9.icd9_id.categ_id.property_account_income_categ_id.id or False
                if not invoice_line_account_id:
                    invoice_line_account_id = ir_property_obj.get('property_account_income_categ_id', 'product.category')
                if not invoice_line_account_id:
                    raise UserError(_('There is no income account defined for this product: "%s". You may have to install a chart of account from Accounting app, settings menu.') % (p_line.service_icd9.icd9_id,))

                tax_ids = []
                taxes = p_line.service_icd9.icd9_id.taxes_id.filtered(lambda r: not p_line.service_icd9.icd9_id.company_id or r.company_id == p_line.service_icd9.icd9_id.company_id)
                tax_ids = taxes.ids

                invoice_line_vals = {
                    'product_id': p_line.service_icd9.icd9_id.display_name,
                    # 'name': p_line.service_icd9.icd9_id.display_name or '',
                    'name': p_line.description_icd9 or '',
                    'origin': p_line.medical_record_id or '',
                    'account_id': invoice_line_account_id,
                    'price_unit': p_line.service_icd9.icd9_id.lst_price,
                    'uom_id': p_line.service_icd9.icd9_id.uom_id.id,
                    'quantity': 1,
                    'product_id': p_line.service_icd9.icd9_id.id,
                    'invoice_id': res.id,
                    'invoice_line_tax_ids': [(6, 0, tax_ids)],
                }


                res1 = account_invoice_line_obj.create(invoice_line_vals)

            inv_list.append(res.id)
            if res:
                imd = self.env['ir.model.data']
                lab_reqs.write({'is_invoiced': True})
                action = imd.xmlid_to_object('account.action_invoice_tree1')
                list_view_id = imd.xmlid_to_res_id('account.invoice_tree')
                form_view_id = imd.xmlid_to_res_id('account.invoice_form')
                result = {

                    'name': action.name,
                    'help': action.help,
                    'type': action.type,
                    'views': [(list_view_id, 'tree'), (form_view_id, 'form')],
                    'target': action.target,
                    'context': action.context,
                    'res_model': action.res_model,
                }

                if res:
                    result['domain'] = "[('id','in',%s)]" % inv_list
        return result

    # vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4: