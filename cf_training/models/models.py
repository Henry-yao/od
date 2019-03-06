# -*- coding: utf-8 -*-

from odoo import models, fields, api

#python 里类继承的写法 （Course新的类名）（models.Model 继承的副类）
#_name 给类赋予一个名字
#_description 类本身的描述，方便后期维护
#_name _description这两个是类变量⬇️
# 同是类的属性，fields.Char通过一个方法返回一个属性 从fields这个类库得到一个Char型字段（Char单行文本，Text多行文本，Html富媒体文本）
#description，这是对这条记录的描述，勿与类描述混淆
#required=True 设置为必填项,视图里写更好控制/灵活 model里写会进数据库
#default 如果没有输入就是用默认值
#fields.Date.today() 是在fields里有一个Date字段自带today函数，取当天日期的值
#Float ；    digits=（6，2）小数精度控制总共六位，保留两位的精度
#Integer
#Boolean 布尔字段
class Course(models.Model):
    _name = 'training.course'
    _description = '培训课程'

    name = fields.Char(string="课程名称",  required=True)
    description = fields.Text(string="课程说明")
    active = fields.Boolean(string="是否有效", default=True)

#one2Many开始第一个字段是与他关联的模型名字（t...g.session , 需要关联的字段, string="名称"）
    session_ids = fields.One2many("training.session", "course_id", string="已开课班级")
#One2many结束
class Session(models.Model):
    _name = 'training.session'
    _description = '开课班级'

    name = fields.Char(string="班级名称", required=True)
#Many2one开始，第一个字段与他关联的模型名字（t..g.course, 名称 , ondelete="cascade"主表删除，从表删掉 ）
#                                                                 "set null"主表删除，这个字段滞空,主表跟从表的关联字段叫required
    course_id = fields.Many2one("training.course", string="培训课程", ondelete="cascade", required=True)

    start_date = fields.Date(string="开班日期", default=fields.Date.today())
    end_date = fields.Date(string="结束时间")
    duration = fields.Float(string="课程时长", digits=(6,2), help='课程持续天数')
    seats = fields.Integer(string="学位数")
    taken_seats = fields.Float(string="已报名人数")
    active = fields.Boolean(string="是否有效", default=True)
    attendees_count = fields.Integer(string="学员数")