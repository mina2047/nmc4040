# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

import time

from odoo import api, fields, models, _
from odoo.exceptions import UserError


class SaleAdvancePaymentInv(models.TransientModel):
    _inherit = "sale.advance.payment.inv"

    def _prepare_invoice_values(self, order, name, amount, so_line):
        invoice_vals = {
        'type': 'out_invoice',
        'invoice_origin': order.name,
        'invoice_user_id': order.user_id.id,
        'company_id': order.company_id.id,
        'narration': order.note,
        'partner_id': order.partner_id.id,
        'fiscal_position_id': order.fiscal_position_id.id or order.partner_id.property_account_position_id.id,
        'partner_shipping_id': order.partner_shipping_id.id,
        'currency_id': order.pricelist_id.currency_id.id,
        'invoice_payment_ref': order.client_order_ref,
        'invoice_payment_term_id': order.payment_term_id.id,
        'invoice_partner_bank_id': order.company_id.partner_id.bank_ids[:1].id,
        'team_id': order.team_id.id,
        'campaign_id': order.campaign_id.id,
        'medium_id': order.medium_id.id,
        'source_id': order.source_id.id,
        'invoice_line_ids': [(0, 0, {
            'name': name,
            'price_unit': amount,
            'quantity': 1.0,
            'product_id': self.product_id.id,
            'product_uom_id': so_line.product_uom.id,
            'tax_ids': [(6, 0, so_line.tax_id.ids)],
            'sale_line_ids': [(6, 0, [so_line.id])],
            'analytic_tag_ids': [(6, 0, so_line.analytic_tag_ids.ids)],
            'analytic_account_id': order.analytic_account_id.id or False,
            'company_id': so_line.company_id.id,
            'term_id': so_line.term_id.id if so_line.term_id else False
            })],
        }

        return invoice_vals

