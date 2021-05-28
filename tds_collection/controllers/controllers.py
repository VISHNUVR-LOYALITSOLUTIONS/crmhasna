# -*- coding: utf-8 -*-
# from odoo import http


# class TdsCollection(http.Controller):
#     @http.route('/tds_collection/tds_collection/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/tds_collection/tds_collection/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('tds_collection.listing', {
#             'root': '/tds_collection/tds_collection',
#             'objects': http.request.env['tds_collection.tds_collection'].search([]),
#         })

#     @http.route('/tds_collection/tds_collection/objects/<model("tds_collection.tds_collection"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('tds_collection.object', {
#             'object': obj
#         })
