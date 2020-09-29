from odoo import models, fields, api

class Staff(models.Model):
    _name = 'staff'
    _description = 'my decripition'

    name = fields.Char(string='Name')
    age = fields.Integer(string='age')
    address = fields.Text(string='Address')
    phone = fields.Char(string='Phone')
    gender = fields.Selection(selection=[('male','Male'),('female','Female')],string='Gender')

class Order(models.Model):
    _name = 'order'

    name = fields.Char(string='Name')
    line_ids = fields.One2many('order.line', 'order_id')


class Orderline(models.Model):
    _name = 'order.line'

    order_id = fields.Many2one('order')
    product_id = fields.Many2one('product.product')
    count = fields.Float(string='Count')



