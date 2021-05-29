# -*- coding: utf-8 -*-
# from odoo import http


# class GstIssueCommunity(http.Controller):
#     @http.route('/gst_issue_community/gst_issue_community/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/gst_issue_community/gst_issue_community/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('gst_issue_community.listing', {
#             'root': '/gst_issue_community/gst_issue_community',
#             'objects': http.request.env['gst_issue_community.gst_issue_community'].search([]),
#         })

#     @http.route('/gst_issue_community/gst_issue_community/objects/<model("gst_issue_community.gst_issue_community"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('gst_issue_community.object', {
#             'object': obj
#         })
