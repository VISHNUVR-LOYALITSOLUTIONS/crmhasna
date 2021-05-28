# -*- coding: utf-8 -*-
# from odoo import http


# class TdsCollectionReport(http.Controller):
#     @http.route('/tds_collection_report/tds_collection_report/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/tds_collection_report/tds_collection_report/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('tds_collection_report.listing', {
#             'root': '/tds_collection_report/tds_collection_report',
#             'objects': http.request.env['tds_collection_report.tds_collection_report'].search([]),
#         })

#     @http.route('/tds_collection_report/tds_collection_report/objects/<model("tds_collection_report.tds_collection_report"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('tds_collection_report.object', {
#             'object': obj
#         })
