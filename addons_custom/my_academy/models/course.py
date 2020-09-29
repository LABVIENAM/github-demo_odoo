from odoo import models, fields

class MyCourse(models.Model):
    _name = 'course'
    _description = 'course model object'
    _rec_name = 'course_name'

    course_name = fields.Char(string='Name of course')
    description = fields.Char()
    fee = fields.Float(string="Fee of course",required='True')
    open_date = fields.Datetime(required='True',string='Open Date', default=lambda self:fields.Datetime.now())