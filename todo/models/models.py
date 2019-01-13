# -*- coding: utf-8 -*-

from odoo import models, fields, api

class TodoTaskCategory(models.Model):
    _name = 'todo.task.category'
    _desciption = "待办事项类别"

    name = fields.Char(string="代办事项类别名称", required=True)
    task_ids = fields.One2many("todo.task", "category_id", string="待办事项")
    task_count = fields.Integer(string="待办事项数量", compute="_compute_task_count")

    @api.depends("task_ids")
    @api.multi
    def _compute_task_count(self):
        for rec in self:
            rec.task_count = len(rec.task_ids)


class TodoTask(models.Model):
    _name = 'todo.task'
    _desciption = "待办事项模块说明"

    name = fields.Char(string="待办事项名称", required=True)
    is_done = fields.Boolean(string="已完成?")
    priority = fields.Selection(
        [('1','普通'),('2','较急'),('3','紧急'),('4','即办')],
        string="优先级", default="1", required=True
    )
    deadline = fields.Datetime(string="截止时间", required=True)
    is_expired = fields.Boolean(string="已过期？",compute="_compute_is_expired")

    category_id = fields.Many2one("todo.task.category", string="事项类别")




    @api.depends("deadline")
    @api.multi
    def _compute_is_expired(self):
        for rec in self:
            if rec.deadline:
                rec.is_expired = rec.deadline < fields.Datetime.now()
            else:
                rec.is_expired = False