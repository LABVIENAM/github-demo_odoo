from odoo import models, fields, api


class OrderCourse(models.Model):
    _name = 'order.course'

    student_id = fields.Many2one(comodel_name='student', string='Student')
    order_date = fields.Datetime(default=fields.Datetime.now())
    total_fee = fields.Float(string='Total Fee', compute='_get_total_fee', readonly='True')
    # session_id = fields.Many2one('session',string='Session')
    course_line_ids = fields.One2many(comodel_name='order.course.line', inverse_name='order_course_id',
                                      string='Order Course List')
    state_register = fields.Selection(selection=[('draft', 'Draft'), ('registed', 'Registed')],
                                      string='State', default='draft')
    note = fields.Char(string='Other Note')

    def validate_register(self):
        self.state_register = 'registed'

    def back_register(self):
        self.state_register = 'draft'

    @api.depends('course_line_ids.sub_total_fee')
    def _get_total_fee(self):
        total_fee = 0
        for line in self.course_line_ids:
            total_fee += line.sub_total_fee
        self.total_fee = total_fee


class OrderCourseLine(models.Model):
    _name = 'order.course.line'

    course_id = fields.Many2one('course', string='Course')
    order_course_id = fields.Many2one('order.course', string='Order Course')
    quantity = fields.Float(string='Quantity')
    fee_course = fields.Float(string='Fee Course')
    sub_total_fee = fields.Float(string='Total Fee', readonly='True')
    note = fields.Char(string='Other Note')
    # state_register = fields.Selection(selection=[('draft', 'Draft'), ('registed', 'Registed')],
    #                                   string='State', default='draft')

    @api.onchange('course_id')
    def _onchange_course_id(self):
        if self.course_id:
            self.quantity = 1
            self.fee_course = self.course_id.fee

    @api.onchange('quantity', 'fee_course')
    def _onchange_total_fee(self):
        self.sub_total_fee = self.quantity * self.fee_course
