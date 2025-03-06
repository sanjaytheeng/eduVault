# -*- coding: utf-8 -*-
# from odoo import http


# class EduvaultElearning(http.Controller):
#     @http.route('/eduvault_elearning/eduvault_elearning', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/eduvault_elearning/eduvault_elearning/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('eduvault_elearning.listing', {
#             'root': '/eduvault_elearning/eduvault_elearning',
#             'objects': http.request.env['eduvault_elearning.eduvault_elearning'].search([]),
#         })

#     @http.route('/eduvault_elearning/eduvault_elearning/objects/<model("eduvault_elearning.eduvault_elearning"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('eduvault_elearning.object', {
#             'object': obj
#         })

