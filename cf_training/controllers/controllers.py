# -*- coding: utf-8 -*-
from odoo import http

# class CfTraining(http.Controller):
#     @http.route('/cf_training/cf_training/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/cf_training/cf_training/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('cf_training.listing', {
#             'root': '/cf_training/cf_training',
#             'objects': http.request.env['cf_training.cf_training'].search([]),
#         })

#     @http.route('/cf_training/cf_training/objects/<model("cf_training.cf_training"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('cf_training.object', {
#             'object': obj
#         })