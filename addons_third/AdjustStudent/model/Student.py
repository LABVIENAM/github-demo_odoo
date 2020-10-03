from odoo import fields, models


class Student(models.Model):
    _inherit = 'student'

    _description = 'student object model'

    parentName = fields.Char(required='True', string='Name of Student')
