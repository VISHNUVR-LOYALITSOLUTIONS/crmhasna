# -*- coding: utf-8 -*-

from odoo import models, fields, api


class L10nInReportAccount(models.AbstractModel):
    _inherit = "l10n.in.report.account"

    def get_gst_section_model_domain(self, gst_return_type, gst_section):
        domain = []
        sum_fields = [
            'account_move_id', 'cess_amount',
            'igst_amount', 'cgst_amount',
            'sgst_amount']
        model = 'l10n_in.account.invoice.report'
        if gst_return_type == 'gstr1':
            domain += [('journal_id.type', '=', 'sale')]
            if gst_section == 'b2b':
                domain += [
                    ('partner_vat', '!=', False),
                    ('l10n_in_export_type', 'in',
                     ['regular', 'deemed', 'sale_from_bonded_wh', 'sez_with_igst', 'sez_without_igst']),
                    ('move_type', 'not in', ('out_refund', 'in_refund'))]
            elif gst_section == 'b2cl':
                domain += [
                    ('partner_vat', '=', False),
                    ('total', '>', '250000'),
                    ('supply_type', '=', 'Inter State'),
                    ('journal_id.l10n_in_import_export', '!=', True),
                    ('move_type', 'not in', ('out_refund', 'in_refund'))]
            elif gst_section == 'b2cs':
                domain += [
                    '&', '&', ('partner_vat', '=', False), ('journal_id.l10n_in_import_export', '!=', True),
                    '|', ('supply_type', '=', 'Intra State'),
                    '&', ('total', '<=', '250000'), ('supply_type', '=', 'Inter State')]
            elif gst_section == 'cdnr':
                domain += [
                    ('partner_vat', '!=', False),
                    ('move_type', 'in', ['out_refund', 'in_refund'])]
            elif gst_section == 'cdnur':
                domain += [
                    ('partner_vat', '=', False),
                    ('total', '>', '250000'), ('supply_type', '=', 'Inter State'),
                    ('journal_id.l10n_in_import_export', '!=', True),
                    ('move_type', 'in', ('out_refund', 'in_refund'))]
            elif gst_section == 'exp':
                domain += [
                    ('journal_id.l10n_in_import_export', '=', True),
                    ('move_type', 'not in', ('out_refund', 'in_refund'))]
            elif gst_section == 'at':
                model = 'l10n_in.advances.payment.report'
                domain = [
                    ('amount', '>', 0),
                    ('payment_type', '=', 'inbound')]
            elif gst_section == 'atadj':
                model = 'l10n_in.advances.payment.adjustment.report'
                domain = [
                    ('payment_type', '=', 'inbound')]
            elif gst_section == 'hsn':
                model = 'l10n_in.product.hsn.report'
            elif gst_section == 'exemp':
                sum_fields = ['account_move_id']
                model = 'l10n_in.exempted.report'
                domain += [
                    ('out_supply_type', '!=', False),
                    '|', ('nil_rated_amount', '!=', 0),
                    '|', ('exempted_amount', '!=', 0),
                    ('non_gst_supplies', '!=', 0)]
            return {'model': model, 'domain': domain}
        return {'model': model, 'domain': domain, 'sum_fields': sum_fields}
