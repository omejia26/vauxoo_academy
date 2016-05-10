# -*- coding: utf-8 -*-
from openerp import http

# class OdooScaffold(http.Controller):
#     @http.route('/odoo_scaffold/odoo_scaffold/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/odoo_scaffold/odoo_scaffold/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('odoo_scaffold.listing', {
#             'root': '/odoo_scaffold/odoo_scaffold',
#             'objects': http.request.env['odoo_scaffold.odoo_scaffold'].search([]),
#         })

#     @http.route('/odoo_scaffold/odoo_scaffold/objects/<model("odoo_scaffold.odoo_scaffold"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('odoo_scaffold.object', {
#             'object': obj
#         })