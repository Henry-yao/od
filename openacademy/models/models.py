# -*- coding: utf-8 -*-

from odoo import models, fields, api, exceptions

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
    start_date = fields.Date(default=fields.Date.today)# （）start_date默认值设置为今天
    duration = fields.Float(digits=(6,2),help="Duration in days")
    seats = fields.Integer(string="Number of seats")
    # 在session中添加一个字段active，并在默认情况下设置为True
    active = fields.Boolean(default=True)

    # 为session选择一个instructor时，只有存在instructor为true到instructor才是可见的
    instructor_id = fields.Many2one('res.partner',string="Instructor",domain=[('instructor', '=', True)])

    #new m2n
    instructor_id = fields.Many2one('res.partner',string="Instructor",domain=['|',('instructor','=',True),('category_id.name','ilike',"Teacher")])
    course_id = fields.Many2one('openacademy.course',ondelet='cascade',string="Course",required=True)

    #new m2m
    attendee_ids = fields.Many2many('res.partner',string="Attendees")

    #将progress字段添加到会话 session增加被占用的椅子字段pro..
    taken_seats = fields.Float(string="Taken seats",compute='_taken_seats')

    @api.depends('seats','attendee_ids')
    def _taken_seats(self):
        for r in self:
            if not r.seats:
                r.taken_seats = 0.0
            else:
                r.taken_seats = 100.0 * len(r.attendee_ids)/r.seats

    # 添加一个显示的onchange方法警告无效值，如负数座位，或participants比seats多的情况
    @api.onchange('seats','attendee_ids')
    def _verify_valid_seats(self):
        if self.seats < 0:
            return {
                'warning':{
                    'title':"Incorrect 'seats' value",
                    'message':"The mumber of available seats may not be negative",
                },
            }
        if self.seats < len(self.attendee_ids):
            return {
                'warning':{
                    'title':"Too many attendees",
                    'message':"Increase seats or remove excess attendees",
                },
            }
    # 添加一个约束用于检查instructor是否参与了他自己的session，import 新加exceptions
    @api.constrains('instructor_id', 'attedee_ids')
    def _check_instructor_not_attendees(self):
        for r in self:
            if r.instructor_id and r.instructor_id in r.attendee_ids:
                raise exceptions.ValidationError("A session's instructor can't be an attendee")