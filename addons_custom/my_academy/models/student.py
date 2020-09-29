from odoo import fields,models

class Student(models.Model):
    _name = 'student'
    _description = 'student object model'
    
    name = fields.Char(required='True',string='Name of Student')
    student_code = fields.Char(required='True', string='Student Code')
    gender = fields.Selection(selection=[('male','Male'),('female','Female')],string='Gender')
    phone = fields.Char(string='Phone Number')
    # course_line_ids = fields.One2many(comodel_name='order.course.line', inverse_name='order_course_id',
    #                                   string='Order Course List')