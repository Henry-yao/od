# -*- coding: utf-8 -*-
from odoo import http

# class CfLicense(http.Controller):
#     @http.route('/cf_license/cf_license/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/cf_license/cf_license/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('cf_license.listing', {
#             'root': '/cf_license/cf_license',
#             'objects': http.request.env['cf_license.cf_license'].search([]),
#         })

#     @http.route('/cf_license/cf_license/objects/<model("cf_license.cf_license"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('cf_license.object', {
#             'object': obj
#         })