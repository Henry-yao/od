# -*- coding: utf-8 -*-

from odoo import models, fields, api, exceptions
from datetime import timedelta

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

    #name有了唯一约束，不能在用duplicate方法来创建副本，实现重新赋值的方法是：使其赋值记录的其他字段，并把新记录的name字段改为【原名称】的副本
    @api.multi
    def copy(self,default=None):
        default = dict(default or {})
        copied_count = self.search_count(
            [('name','=like',u"Copy of {}%".format(self.name))]
        )
        if not copied_count:
            new_name = u"Copy of {}".format(self.name)
        else:
            new_name = u"Copy of {} ({})".format(self.name,copied_count)
        default['name'] = new_name
        return super(Course, self).copy(default)

    #添加SQL约束：检查course的description和title是否不同，course的名字不能重复
    _sql_constraints = [
        ('name_description_check',
         'CHECK(name != description)',
         "The title of the course should not be the description"),

        ('name_unique',
         'UNIQUE(name)',
         "The course title must be unique"),
    ]

# session类
class Session(models.Model):
    _name = 'openacademy.session'
    name = fields.Char(required=True)
    start_date = fields.Date(default=fields.Date.today)# （）start_date默认值设置为今天
    duration = fields.Float(digits=(6,2),help="Duration in days")
    seats = fields.Integer(string="Number of seats")


    # 增加attendees为一个储存在数据库中的计算型字段


    # 在session中添加一个字段active，并在默认情况下设置为True
    active = fields.Boolean(default=True)
#看板 x# 看板，在session增加 color ,更新到action
    color = fields.Integer(string="color")

    # 为session选择一个instructor时，只有存在instructor为true到instructor才是可见的
    instructor_id = fields.Many2one('res.partner',string="Instructor",domain=[('instructor', '=', True)])

    #new m2n
    instructor_id = fields.Many2one('res.partner',string="Instructor",domain=['|',('instructor','=',True),('category_id.name','ilike',"Teacher")])
    course_id = fields.Many2one('openacademy.course',ondelet='cascade',string="Course",required=True)

    #new m2m
    attendee_ids = fields.Many2many('res.partner',string="Attendees")

    #将progress字段添加到会话 session增加被占用的椅子字段pro..
    taken_seats = fields.Float(string="Taken seats",compute='_taken_seats')

    #日程表：增加一个end_date字段，由start_date和duration 计算得出
    end_date = fields.Date(string="End Date", store=True, compute='_get_end_date', inverse='_set_end_date')

    # 创建一个计算型字段用来计算session的持续时间
    hours = fields.Float(string="Duration in hours", compute='_get_hours', inverse='_set_hours')

    attendees_count = fields.Integer(
        string="Attendees count", compute='_get_attendees_count', store=True
    )
    @api.depends('seats','attendee_ids')
    def _taken_seats(self):
        for r in self:
            if not r.seats:
                r.taken_seats = 0.0
            else:
                r.taken_seats = 100.0 * len(r.attendee_ids)/r.seats

    # # 增加一个end_date字段。由start_date and duration jisuanchu
    # @api.depends('start_date', 'duration')
    # def _get_end_date(self):
    #     for r in self:
    #         if not (r.start_date and r.duration):
    #             r.end_date = r.start_date
    #             continue
    #
    #             start = fields.Datetime.from_string(r.start_date)
    #             duration = timedelta(days=r.duration, seconds=-1)
    #             r.end_date = start + duration
    #     def _set_end_date(self):
    #         for r in self:
    #             if not (r.start_date and r.end_date):
    #                 continue
    #
    #                 start_date = fields.Datetime.from_string(r.start_date)
    #                 end_date = fields.Datetime.from_string(r.end_date)
    #                 r.duration = (end_date - start_date).days + 1

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

    # 增加一个end_date字段。由start_date and duration jisuanchu
    @api.depends('start_date', 'duration')
    def _get_end_date(self):
        for r in self:
            if not (r.start_date and r.duration):
                r.end_date = r.start_date
                continue

                start = fields.Datetime.from_string(r.start_date)
                duration = timedelta(days=r.duration, seconds=-1)
                r.end_date = start + duration
    def _set_end_date(self):
        for r in self:
            if not (r.start_date and r.end_date):
                continue

                start_date = fields.Datetime.from_string(r.start_date)
                end_date = fields.Datetime.from_string(r.end_date)
                r.duration = (end_date - start_date).days + 1

    # session的持续时间，创建一个计算型字段
    @api.depends('duration')
    def _get_hours(self):
        for r in self:
            r.hours = r.duration * 24

    def _set_hours(self):
        for r in self:
            r.duration = r.hours / 24
    #     # 增加attendees为一个储存在数据库中的计算型字段

    # 增加 attendees 为一个储存在数据库中的计算型字段。
    @api.depends('attendee_ids')
    def _get_attendees_count(self):
        for r in self:
            r.attendee_count = len(r.attendee_ids)

    # 添加一个约束用于检查instructor是否参与了他自己的session，import 新加exceptions
    @api.constrains('instructor_id', 'attedee_ids')
    def _check_instructor_not_attendees(self):
        for r in self:
            if r.instructor_id and r.instructor_id in r.attendee_ids:
                raise exceptions.ValidationError("A session's instructor can't be an attendee")


