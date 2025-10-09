# -*- coding: utf-8 -*-
# from odoo import http


# class SafrialLatihan(http.Controller):
#     @http.route('/safrial_latihan/safrial_latihan', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/safrial_latihan/safrial_latihan/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('safrial_latihan.listing', {
#             'root': '/safrial_latihan/safrial_latihan',
#             'objects': http.request.env['safrial_latihan.safrial_latihan'].search([]),
#         })

#     @http.route('/safrial_latihan/safrial_latihan/objects/<model("safrial_latihan.safrial_latihan"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('safrial_latihan.object', {
#             'object': obj
#         })

