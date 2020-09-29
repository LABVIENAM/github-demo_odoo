from odoo import models, fields, api


class Customer(models.Model):
    _name = 'customer'
    _description = 'Customer Object Model'

    # odoo tu dong nhan dien field 'name'. Khuyen cao khong nen viet ten field khac 'name'
    name = fields.Char(string='Name')
    address = fields.Text(string='Address')
    phone = fields.Char(string='Phone')
    gender = fields.Selection(selection=[('male', 'Male'), ('female', 'Female')],
                              string='Gender')