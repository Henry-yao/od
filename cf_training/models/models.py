# -*- coding: utf-8 -*-

from datetime import datetime,timedelta
from odoo import models, fields, api


#模型合作伙伴的继承扩展 course老师和培训课程多对多 session学生对班级多对多
# _inherit 继承哪个模块
# instructor属性字段 要创建到表的名字：instructor_course_ids指明这个中间表，不指明自动生成有时候会很长
#Many2many多对多字段,第一个属性是关联到哪个对象上（"training.course"）
# column1 partner这个模型里表里生成的字段名字是 instructor_id
# column2="course_id" 表示training.course里的组建
# string 字段标签
class Respartiner(models.Model):
    _inherit = "res.partner"
    instructor = fields.Boolean(string="是讲师？", default=False)
    instructor_course_ids = fields.Many2many("training.course",
                                             relation="instructor_course_rel",
                                             column1="instructor_id",
                                             column2="course_id",
                                             string="主讲课程")

    attendee_session_ids = fields.Many2many("training.session",
                                            relation="attend_session_rel",
                                            column1="attendee_id",
                                            column2="session_id",
                                            string="参训班级")

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
#Integer 整数
#Boolean 布尔字段
class Course(models.Model):
    _name = 'training.course'
    _description = '培训课程'

    name = fields.Char(string="课程名称",  required=True)
    description = fields.Text(string="课程说明")
    active = fields.Boolean(string="是否有效", default=True)
#Many2one开始，res.users 中的users是partner的子类
    responsible_id = fields.Many2one("res.users", ondelete='set null', string='负责人', index=True)
#one2Many开始第一个字段是与他关联的模型名字（t...g.session , 需要关联的字段, string="名称"）
    session_ids = fields.One2many("training.session", "course_id", string="已开课班级")
#One2many结束
class Session(models.Model):
    _name = 'training.session'
    _description = '开课班级'

# 装饰器api 用来计算compute；def定义一个方法；通过开始日期跟开始时常计算
#依赖什么字段@api.depends("start_date", "duration") depends就是依赖的意思。写的话如果depends无值的时候写的话就不会空计算
#rec 是简写
#要加一个python的类 form datetime import datetime,timedelta
#timedelta(days=rec.duration)通过日期里面把天取出来
#@api.multi 装饰器 把传进来的参数self 有可能是单条记录还是记录集，multi全部组成数组当成多条记录，让for in 正常循环
# continue 继续下一条记录
# 开始日期+ 天数 = 截止日期
#计算字段不能拿来搜索条件 查询条件 search字段 写一个方法实现搜索
    @api.multi
    @api.depends("start_date", "duration")
    def _compute_end_date(self):
        for rec in self:
            if not (rec.start_date and rec.end_date):
            rec.end_date = rec.start_date
            continue

            duration = timedelta(days=rec.duration)
            rec.end_date = rec.start_date + duration

#search 写一个方法实现搜索 计算字段的搜索函数名字：_search_end_date
#函数穿进去会调用3个参数，self当前记录，operator运算符，value搜索传入的参数值
#operator 判断运算符是否正确，如果不在范围就不管，
#_value 对搜索日期值格式化，按照括号里转化；strptime是python里日期处理，把字符串转成日期
#把datetime转出来对日期 把查询的减去课时天数，得到要查询的起始日期
    def _search_end_date(self, operator, value):
        if operator not in ('=', '!=', '<', '<=', '>', '>=', 'in', 'not in')
            return []

        _value = datetime.strptime(value, '%Y-%m-%d %H:%M:%S')

        _start_date = value + timedelta(days=self.duration*(-1)) #把查询的减去课时天数，得到要查询的起始日期
        return [('start_date', operator, _start_date)] #dom表达式

#学员数compute=_compute_attendees_count计算方法
    @api.multi
    @api.depends("attendee_ids")
    def _compute_attendees_count(self):
        for rec in self:
            rec.attendees_count = len(rec.attendee_ids)
#上面的方法说明：获取attendee_ids的数量 得到 attendees_count的数量，这里用到python的len方法


# 报名比例compute=_compute_taken_seats计算方法
    @api.multi
    @api.depends("seats", "attendees_count")
    def _compute_taken_seats(self):
        for rec in self:
            rec.taken_seats = 100 * len(rec.attendee_ids) / rec.seats

    name = fields.Char(string="班级名称", required=True)
#Many2one开始，第一个字段与他关联的模型名字（t..g.course, 名称 , ondelete="cascade"主表删除，从表删掉 ）
#                                                                 "set null"主表删除，这个字段滞空,主表跟从表的关联字段叫required
#     course_id = fields.Many2one("training.course", string="培训课程", ondelete="cascade", required=True)
    duration = fields.Float(string="课程时长", digits=(6, 2), help='课程持续天数')
    start_date = fields.Date(string="开班日期", default=fields.Date.today())
# compute字段表示计算 通过方法指定_compute_end_date
    end_date = fields.Date(string="结束时间", compute=_compute_end_date, search=_search_end_date)#search 写一个方法实现搜索#必要的时候加上store=True 就可以存到库
    seats = fields.Integer(string="学位数")
    taken_seats = fields.Float(string="报名比例", compute=_compute_taken_seats)# 通过compute 来计算比例要写一个方法
#Many2many字段解释：column1=本表字段（在中间表存储字段名字；column2=在中间表学员ID；中间表是res.partner表
    attendees_ids = fields.Many2many("res.partner", column1='session_id', column2='attendee_id', string='参训学员')
    attendees_count = fields.Integer(string="学员数", compute=_compute_attendees_count)#加上compute，attendees_ids有几条记录，那么学员数就是几；并写一条方法。多用自动计算数据不容易乱
    active = fields.Boolean(string="是否有效", default=True)