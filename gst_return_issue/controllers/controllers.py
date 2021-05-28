# -*- coding: utf-8 -*-
# from odoo import http


# class GstReturnIssue(http.Controller):
#     @http.route('/gst_return_issue/gst_return_issue/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/gst_return_issue/gst_return_issue/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('gst_return_issue.listing', {
#             'root': '/gst_return_issue/gst_return_issue',
#             'objects': http.request.env['gst_return_issue.gst_return_issue'].search([]),
#         })

#     @http.route('/gst_return_issue/gst_return_issue/objects/<model("gst_return_issue.gst_return_issue"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('gst_return_issue.object', {
#             'object': obj
#         })
