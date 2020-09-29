# -*- coding: utf-8 -*-
from odoo import models, fields, api
from odoo.exceptions import ValidationError


class Customer(models.Model):
    _name = 'customer'
    _description = 'Customer Object Model'

    # odoo tu dong nhan dien field 'name'. Khuyen cao khong nen viet ten field khac 'name'
    name = fields.Char(string='Name')
    address = fields.Text(string='Address')
    phone = fields.Char(string='Phone')
    gender = fields.Selection(selection=[('male', 'Male'), ('female', 'Female')],
                              string='Gender')
    order_ids = fields.One2many('orders', 'customer_id', string='Orders')

    # raise ValidationError('Message Display')
    @api.model
    def create(self, vals):
        vals['name'] = vals['name'].title()
        vals['name'] = vals['name'] + ' PYAE0519'
        if not vals.get('address', ''):
            vals['address'] = 'Ha Noi'
        return super(Customer, self).create(vals)

    # @api.multi
    def write(self, vals):
        if vals.get('name', False):
            vals['name'] = vals['name'].replace('PYAE0519', '').strip()
        if not vals.get('address', False):
            raise ValidationError('Please Update The Address')
        if not vals.get('gender', False):
            vals['gender'] = 'male'
        return super(Customer, self).write(vals)
