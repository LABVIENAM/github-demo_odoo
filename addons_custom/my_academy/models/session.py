from odoo import fields, models, api, exceptions


class Session(models.Model):
    _name = 'session'
    _description = 'session model object'

    name = fields.Char(default="Programming Register", required=True)
    start_date = fields.Date(default=fields.Date.today)
    duration = fields.Float(digits=(6, 2), default="12", help="Duration in days")
    seats = fields.Integer(string="Seats")
    total_seat = fields.Integer(string="Total Seat")
    color = fields.Integer()
    course_regis = fields.Many2one(comodel_name="course")

    # total_fee = fields.Float(string='Total fee',compute='_get_total_fee',store='True')
    student_ids = fields.Many2many(comodel_name='student', string='Student')

    # course_line_ids = fields.One2many(comodel_name='order.course', inverse_name='session_id', string='Order Course List')
    # note = fields.Char(string='Other Note')
    # state_register = fields.Selection(selection=[('draft','Draft'),('registed','Registed')],
                                     # string='State', default='draft')

    # @api.depends('course_line_ids.total_fee')
    # def _get_total_fee(self):
    #     total_fee = 0
    #     for line in self.course_line_ids:
    #         total_fee += line.total_fee
    #     self.total_fee = total_fee
    #
    # def validate_register(self):
    #     self.state_register = 'registed'
    #
    # @api.onchange('student_ids')
    # def _onchange_student_ids(self):
    #     if self.student_ids:
    #         self.seats += self.seats
    #     print("aaaaaaass ", self.seats)
        # seats = 0
        # for line in self:
        #     seats = line.seats + 1
        # self.seats = seats

    # @api.onchange('total_seat')
    # def _onchange_total_seats(self):

    @api.onchange('total_seat', 'student_ids')
    def _onchange_seats(self):
        if self.total_seat < 0:
            return {'warning': {
                'title': "Incorect total seat value",
                'message': "The number of available seats may not be negatevie"
            }
            }
        if len(self.student_ids) > self.total_seat:
            return {
                'warning': {
                    'title': "Incorect seat value",
                    'message': "The number of available seats may not be less than total seat"
                }
            }
