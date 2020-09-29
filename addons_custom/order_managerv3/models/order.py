# -*- coding: utf-8 -*-
# __author__ = 'ITplus'


from odoo import models, fields, api
from odoo.exceptions import ValidationError


class Order(models.Model):
    _name = 'orders'

    name = fields.Char(string='Name')
    order_date = fields.Datetime(string='Order Date',
                                 default=lambda self: fields.Datetime.now())
    total_amount = fields.Float(string='Total amount', compute='_get_total_amount', store=True)
    customer_id = fields.Many2one(comodel_name='customer', string='Customer')
    line_ids = fields.One2many(comodel_name='order.line',
                               inverse_name='order_id', string='Order Lines')
    state = fields.Selection(selection=[('draft', 'Draft'), ('paid', 'Paid')],
                             string='States', default='draft')

    # @api.multi
    @api.depends('line_ids.sub_total')
    def _get_total_amount(self):
        for order in self:
            total_amount = 0
            for line in order.line_ids:
                total_amount += line.sub_total
            order.total_amount = total_amount

    # @api.multi
    def validate_order(self):
        self.state = 'paid'

    @api.model
    def create(self, vals):
        vals['name'] = vals['name'] + ' ITPLUS'
        return super(Order, self).create(vals)

    # @api.multi
    def write(self, vals):
        return super(Order, self).write(vals)

    # @api.multi
    def unlink(self):
        if self.state == 'paid':
            raise ValidationError('Can\'t delete this order')
            # raise ValidationError("Can't delete this order")
        return super(Order, self).unlink()
