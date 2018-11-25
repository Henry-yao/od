# -*- coding: utf-8 -*-

from odoo import models, fields, api

# class openacademy(models.Model):
#     _name = 'openacademy.openacademy'

#     name = fields.Char()
#     value = fields.Integer()
#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()
#
#     @api.depends('value')
#     def _value_pc(self):
#         self.value2 = float(self.value) / 100
# 新建一个course实例
class Course(models.Model):
    _name = 'openacademy.course'
    name = fields.Char(string='Title',required=True)
    description = fields.Text()
    #new m2n type
    responsible_id = fields.Many2one('res.users',ondelete='set null',string="Responsible",index=True)
    #new o2m
    session_ids = fields.One2many('openacademy.session','course_id',string="Sessions")
# session类
class Session(models.Model):
    _name = 'openacademy.session'
    name = fields.Char(required=True)
    start_date = fields.Date()
    duration = fields.Float(digits=(6,2),help="Duration in days")
    seats = fields.Integer(string="Number of seats")
    # 为session选择一个instructor时，只有存在instructor为true到instructor才是可见的
    instructor_id = fields.Many2one('res.partner',string="Instructor",domain=[('instructor', '=', True)])
    course_id = fields.Many2one()
    #new m2n
    instructor_id = fields.Many2one('res.partner',string="Instructor")
    course_id = fields.Many2one('openacademy.course',ondelet='cascade',string="Course",required=True)
    #new m2m
    attendee_ids = fields.Many2many('res.partner',string="Attendees")