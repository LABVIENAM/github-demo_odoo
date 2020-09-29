from odoo import models, fields, api


class Products(models.Model):
    _name = 'products'
    _rec_name = 'product_name'

    product_name = fields.Char(string='Name')
    description = fields.Char(string='Description')
    date = fields.Datetime(string='Date',
                           default=lambda self: fields.Datetime.now())
    price = fields.Float(string='Price')
