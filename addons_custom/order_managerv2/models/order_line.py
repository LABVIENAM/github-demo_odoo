# __author__ = 'ITplus'

from odoo import models, fields, api


class OrderLine(models.Model):
    _name = 'order.line'

    created_date = fields.Datetime(string='Created Date')
    qty = fields.Float(string='Quantity')
    amount = fields.Float(string='Amount')
    order_id = fields.Many2one('orders', string='Order')
    sub_total = fields.Float(string='Total', readonly=True)
    product_id = fields.Many2one('products', string='Product')

    @api.onchange('product_id')
    def onchange_product_id(self):
        if self.product_id:
            self.qty = 1
            self.amount = self.product_id.price

    @api.onchange('qty', 'amount')
    def onchange_total(self):
        self.sub_total = self.qty * self.amount
