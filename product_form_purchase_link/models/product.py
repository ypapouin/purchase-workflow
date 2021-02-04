# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from datetime import timedelta

from odoo import api, fields, models, _
from odoo.tools.float_utils import float_round

# class ProductTemplate(models.Model):
#     _name = 'product.template'
#     _inherit = 'product.template'

#     @api.multi
#     def _compute_purchased_product_qty(self):
#         for template in self:
#             template.purchased_product_qty = float_round(sum([p.purchased_product_qty for p in template.product_variant_ids]), precision_rounding=template.uom_id.rounding)


class ProductProduct(models.Model):
    _name = 'product.product'
    _inherit = 'product.product'

    @api.multi
    def _compute_purchased_product_qty(self):
        domain = [
            ('state', 'in', ['purchase', 'done']),
            ('product_id', 'in', self.mapped('id')),
        ]
        # PurchaseOrderLines = self.env['purchase.order.line'].search(domain)
        order_lines = self.env['purchase.order.line'].read_group(domain, ['product_id', 'product_uom_qty'], ['product_id'])
        purchased_data = dict([(data['product_id'][0], data['product_uom_qty']) for data in order_lines])
        for product in self:
            product.purchased_product_qty = float_round(purchased_data.get(product.id, 0), precision_rounding=product.uom_id.rounding)
