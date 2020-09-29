from odoo import models,fields, api

class Student(models.Model):
    _name = 'student'
    _description = 'test decription'

    name=fields.Char(string='Name')
    class_id=fields.One2many(string='Class ID')
    age=fields.Integer(int='age')
    gender=fields.Char(string='Male/Female')

class Class(models.Model):
    _name = 'class'
    _description = 'decription class'

    name=fields.Char(string='Class Name')
    code=fields.NewId(string='Class Code')
    student_id=fields.Many2one(string='Student ID')
    amount=fields.Interger(string='Amount')