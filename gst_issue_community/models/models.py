# -*- coding: utf-8 -*-

from odoo import models, fields, api, tools


# class L10nInAccountInvoiceReport(models.Model):
#     _inherit = "l10n_in.account.invoice.report"
#
#     def _select(self):
#         select_str = """
#             SELECT min(sub.id) as id,
#             sub.move_id,
#             sub.account_move_id,
#             sub.name,
#             sub.state,
#             sub.partner_id,
#             sub.date,
#             sub.l10n_in_export_type,
#             sub.ecommerce_partner_id,
#             sub.shipping_bill_number,
#             sub.shipping_bill_date,
#             sub.shipping_port_code_id,
#             sub.total * sub.b2cs_refund_sign as total,
#             sub.journal_id,
#             sub.company_id,
#             sub.move_type,
#             sub.reversed_entry_id,
#             sub.partner_vat,
#             sub.ecommerce_vat,
#             sub.tax_rate as tax_rate,
#             (CASE WHEN count(sub.is_reverse_charge) > 0
#                 THEN 'Y'
#                 ELSE 'N'
#                 END) AS is_reverse_charge,
#             sub.place_of_supply,
#             sub.is_pre_gst,
#             sub.is_ecommerce,
#             sub.b2cl_is_ecommerce,
#             sub.b2cs_is_ecommerce,
#             sub.supply_type,
#             sub.export_type,
#             sub.refund_export_type,
#             sub.b2b_type,
#             sub.refund_invoice_type,
#             sub.gst_format_date,
#             sub.gst_format_refund_date,
#             sub.gst_format_shipping_bill_date,
#             sum(sub.igst_amount) * sub.amount_sign * sub.b2cs_refund_sign AS igst_amount,
#             sum(sub.cgst_amount) * sub.amount_sign * sub.b2cs_refund_sign AS cgst_amount,
#             sum(sub.sgst_amount) * sub.amount_sign * sub.b2cs_refund_sign AS sgst_amount,
#             avg(sub.cess_amount) * sub.amount_sign * sub.b2cs_refund_sign AS cess_amount,
#             sum(sub.price_total) * sub.amount_sign * sub.b2cs_refund_sign AS price_total,
#             sub.tax_id
#         """
#         return select_str
#
#     def _sub_select(self):
#         sub_select_str = """
#             SELECT aml.id AS id,
#                 aml.move_id,
#                 aml.partner_id,
#                 am.id AS account_move_id,
#                 am.name,
#                 am.state,
#                 am.date,
#                 am.l10n_in_export_type AS l10n_in_export_type,
#                 am.l10n_in_reseller_partner_id AS ecommerce_partner_id,
#                 am.l10n_in_shipping_bill_number AS shipping_bill_number,
#                 am.l10n_in_shipping_bill_date AS shipping_bill_date,
#                 am.l10n_in_shipping_port_code_id AS shipping_port_code_id,
#                 ABS(am.amount_total_signed) AS total,
#                 am.journal_id,
#                 aj.company_id,
#                 am.type AS move_type,
#                 am.reversed_entry_id AS reversed_entry_id,
#                 p.vat AS partner_vat,
#                 CASE WHEN rp.vat IS NULL THEN '' ELSE rp.vat END AS ecommerce_vat,
#                 (CASE WHEN at.l10n_in_reverse_charge = True
#                     THEN True
#                     ELSE NULL
#                     END)  AS is_reverse_charge,
#                 (CASE WHEN ps.l10n_in_tin IS NOT NULL
#                     THEN concat(ps.l10n_in_tin,'-',ps.name)
#                     WHEN ps.id IS NULL and cps.l10n_in_tin IS NOT NULL
#                     THEN concat(cps.l10n_in_tin,'-',cps.name)
#                     ELSE ''
#                     END) AS place_of_supply,
#                 (CASE WHEN am.type in ('out_refund', 'in_refund') and refund_am.date <= to_date('2017-07-01', 'YYYY-MM-DD')
#                     THEN 'Y'
#                     ELSE 'N'
#                     END) as is_pre_gst,
#                 (CASE WHEN am.l10n_in_reseller_partner_id IS NOT NULL
#                     THEN 'Y'
#                     ELSE 'N'
#                     END) as is_ecommerce,
#                 (CASE WHEN am.l10n_in_reseller_partner_id IS NOT NULL
#                     THEN 'Y'
#                     ELSE 'N'
#                     END) as b2cl_is_ecommerce,
#                 (CASE WHEN am.l10n_in_reseller_partner_id IS NOT NULL
#                     THEN 'E'
#                     ELSE 'OE'
#                     END) as b2cs_is_ecommerce,
#                 (CASE WHEN ps.id = cp.state_id or p.id IS NULL
#                     THEN 'Intra State'
#                     WHEN ps.id != cp.state_id and p.id IS NOT NULL
#                     THEN 'Inter State'
#                     END) AS supply_type,
#                 (CASE WHEN am.l10n_in_export_type in ('deemed', 'export_with_igst', 'sez_with_igst')
#                     THEN 'EXPWP'
#                     WHEN am.l10n_in_export_type in ('sale_from_bonded_wh', 'sez_without_igst')
#                     THEN 'EXPWOP'
#                     ELSE ''
#                     END) AS export_type,
#                 (CASE WHEN refund_am.l10n_in_export_type in ('deemed', 'export_with_igst', 'sez_with_igst')
#                     THEN 'EXPWP'
#                     WHEN refund_am.l10n_in_export_type in ('sale_from_bonded_wh', 'sez_without_igst')
#                     THEN 'EXPWOP'
#                     ELSE 'B2CL'
#                     END) AS refund_export_type,
#                 (CASE WHEN am.l10n_in_export_type = 'regular'
#                     THEN 'Regular'
#                     WHEN am.l10n_in_export_type = 'deemed'
#                     THEN 'Deemed'
#                     WHEN am.l10n_in_export_type = 'sale_from_bonded_wh'
#                     THEN 'Sale from Bonded WH'
#                     WHEN am.l10n_in_export_type = 'export_with_igst'
#                     THEN 'Export with IGST'
#                     WHEN am.l10n_in_export_type = 'sez_with_igst'
#                     THEN 'SEZ with IGST payment'
#                     WHEN am.l10n_in_export_type = 'sez_without_igst'
#                     THEN 'SEZ without IGST payment'
#                     END) AS b2b_type,
#                 (CASE WHEN am.type = 'out_refund'
#                     THEN 'C'
#                     WHEN am.type = 'in_refund'
#                     THEN 'D'
#                     ELSE ''
#                     END) as refund_invoice_type,
#                 (CASE WHEN am.date IS NOT NULL
#                     THEN TO_CHAR(am.date, 'DD-MON-YYYY')
#                     ELSE ''
#                     END) as gst_format_date,
#                 (CASE WHEN refund_am.date IS NOT NULL
#                     THEN TO_CHAR(refund_am.date, 'DD-MON-YYYY')
#                     ELSE ''
#                     END) as gst_format_refund_date,
#                 (CASE WHEN am.l10n_in_shipping_bill_date IS NOT NULL
#                     THEN TO_CHAR(am.l10n_in_shipping_bill_date, 'DD-MON-YYYY')
#                     ELSE ''
#                     END) as gst_format_shipping_bill_date,
#                 CASE WHEN tag_rep_ln.account_tax_report_line_id IN
#                     (SELECT res_id FROM ir_model_data WHERE module='l10n_in' AND name='tax_report_line_igst')
#                     THEN aml.balance
#                     ELSE 0
#                     END AS igst_amount,
#                 CASE WHEN tag_rep_ln.account_tax_report_line_id IN
#                     (SELECT res_id FROM ir_model_data WHERE module='l10n_in' AND name='tax_report_line_cgst')
#                     THEN aml.balance
#                     ELSE 0
#                     END AS cgst_amount,
#                 CASE WHEN tag_rep_ln.account_tax_report_line_id IN
#                     (SELECT res_id FROM ir_model_data WHERE module='l10n_in' AND name='tax_report_line_sgst')
#                     THEN aml.balance
#                     ELSE 0
#                     END AS sgst_amount,
#                 (SELECT sum(temp_aml.balance) from account_move_line temp_aml
#                     JOIN account_account_tag_account_move_line_rel aat_aml_rel_temp ON aat_aml_rel_temp.account_move_line_id = temp_aml.id
#                     JOIN account_account_tag aat_temp ON aat_temp.id = aat_aml_rel_temp.account_account_tag_id
#                     JOIN account_tax_report_line_tags_rel tag_rep_ln_temp ON aat_temp.id = tag_rep_ln_temp.account_account_tag_id
#                     where temp_aml.move_id = aml.move_id and temp_aml.product_id = aml.product_id
#                     and tag_rep_ln_temp.account_tax_report_line_id IN (SELECT res_id FROM ir_model_data WHERE module='l10n_in' AND name='tax_report_line_cess')
#                     ) AS cess_amount,
#                 CASE WHEN tag_rep_ln.account_tax_report_line_id IN
#                     (SELECT res_id FROM ir_model_data WHERE module='l10n_in' AND name='tax_report_line_sgst') OR at.l10n_in_reverse_charge = True
#                     THEN NULL
#                     ELSE (CASE WHEN aml.tax_base_amount <> 0 THEN aml.tax_base_amount * (CASE WHEN aml.balance < 0 THEN -1 ELSE 1 END) ELSE NULL END)
#                     END AS price_total,
#                 (CASE WHEN aj.type = 'sale' AND (am.type IS NULL OR am.type != 'out_refund') THEN -1 ELSE 1 END) AS amount_sign,
#                 (CASE WHEN am.type in ('in_refund','out_refund')
#                     AND p.vat IS NULL
#                     AND (aj.l10n_in_import_export IS NULL or aj.l10n_in_import_export = false)
#                     AND (ABS(am.amount_total_signed) <= 250000 OR
#                     (ps.id = cp.state_id OR p.id IS NULL))
#                     THEN -1
#                     ELSE 1 END) AS b2cs_refund_sign,
#                 (CASE WHEN atr.parent_tax IS NOT NULL THEN atr.parent_tax
#                     ELSE at.id END) AS tax_id,
#                 (CASE WHEN atr.parent_tax IS NOT NULL THEN parent_at.amount
#                     ELSE at.amount END) AS tax_rate
#         """
#         return sub_select_str
#
#     def _group_by(self):
#         group_by_str = """
#         GROUP BY sub.move_id,
#             sub.account_move_id,
#             sub.name,
#             sub.state,
#             sub.partner_id,
#             sub.date,
#             sub.l10n_in_export_type,
#             sub.ecommerce_partner_id,
#             sub.shipping_bill_number,
#             sub.shipping_bill_date,
#             sub.shipping_port_code_id,
#             sub.total,
#             sub.journal_id,
#             sub.company_id,
#             sub.move_type,
#             sub.reversed_entry_id,
#             sub.partner_vat,
#             sub.ecommerce_vat,
#             sub.place_of_supply,
#             sub.is_pre_gst,
#             sub.is_ecommerce,
#             sub.b2cl_is_ecommerce,
#             sub.b2cs_is_ecommerce,
#             sub.supply_type,
#             sub.export_type,
#             sub.refund_export_type,
#             sub.b2b_type,
#             sub.refund_invoice_type,
#             sub.gst_format_date,
#             sub.gst_format_refund_date,
#             sub.gst_format_shipping_bill_date,
#             sub.amount_sign,
#             sub.tax_id,
#             sub.tax_rate,
#             sub.b2cs_refund_sign
#         """
#         return group_by_str


class L10nInProductHsnReport(models.Model):
    _inherit = "l10n_in.product.hsn.report"

    def _select(self):
        select_str = """SELECT max(id) as id,
            account_move_id,
            partner_id,
            product_id,
            max(uom_id) as uom_id,
            date,
            journal_id,
            company_id,
            hsn_code,
            hsn_description,
            max(l10n_in_uom_code) as l10n_in_uom_code,
            sum(quantity) AS quantity,
            sum(igst_amount) AS igst_amount,
            sum(cgst_amount) AS cgst_amount,
            sum(sgst_amount) AS sgst_amount,
            sum(cess_amount) AS cess_amount,
            sum(price_total) AS price_total,
            sum(total) AS total
        """
        return select_str

    def _sub_select(self):
        sub_select_str = """SELECT aml.id AS id,
            aml.move_id AS account_move_id,
            aml.partner_id AS partner_id,
            aml.product_id,
            aml.product_uom_id AS uom_id,
            am.date,
            am.journal_id,
            aj.company_id,
            CASE WHEN pt.l10n_in_hsn_code IS NULL THEN '' ELSE pt.l10n_in_hsn_code END AS hsn_code,
            CASE WHEN pt.l10n_in_hsn_description IS NULL THEN '' ELSE pt.l10n_in_hsn_description END AS hsn_description,
            CASE WHEN uom.l10n_in_code IS NULL THEN '' ELSE uom.l10n_in_code END AS l10n_in_uom_code,
            CASE WHEN aml.tax_line_id IS NULL
                THEN aml.quantity
                ELSE 0
                END AS quantity,
            CASE WHEN tag_rep_ln.account_tax_report_line_id IN
                (SELECT res_id FROM ir_model_data WHERE module='l10n_in' AND name='tax_report_line_igst')
                THEN aml.balance * (CASE WHEN aj.type = 'sale' THEN -1 ELSE 1 END)
                ELSE 0
                END AS igst_amount,
            CASE WHEN tag_rep_ln.account_tax_report_line_id IN
                (SELECT res_id FROM ir_model_data WHERE module='l10n_in' AND name='tax_report_line_cgst')
                THEN aml.balance * (CASE WHEN aj.type = 'sale' THEN -1 ELSE 1 END)
                ELSE 0
                END AS cgst_amount,
            CASE WHEN tag_rep_ln.account_tax_report_line_id IN
                (SELECT res_id FROM ir_model_data WHERE module='l10n_in' AND name='tax_report_line_sgst')
                THEN aml.balance * (CASE WHEN aj.type = 'sale' THEN -1 ELSE 1 END)
                ELSE 0
                END AS sgst_amount,
            CASE WHEN tag_rep_ln.account_tax_report_line_id IN
                (SELECT res_id FROM ir_model_data WHERE module='l10n_in' AND name='tax_report_line_cess')
                THEN aml.balance * (CASE WHEN aj.type = 'sale' THEN -1 ELSE 1 END)
                ELSE 0
                END AS cess_amount,
            CASE WHEN aml.tax_line_id IS NULL
                THEN (aml.balance * (CASE WHEN aj.type = 'sale' THEN -1 ELSE 1 END))
                ELSE 0
                END AS price_total,
            (aml.balance * (CASE WHEN aj.type = 'sale' THEN -1 ELSE 1 END))  AS total
        """
        return sub_select_str

    def _from(self):
        from_str = """FROM account_move_line aml
            JOIN account_move am ON am.id = aml.move_id
            JOIN account_account aa ON aa.id = aml.account_id
            JOIN account_journal aj ON aj.id = am.journal_id
            JOIN product_product pp ON pp.id = aml.product_id
            JOIN product_template pt ON pt.id = pp.product_tmpl_id
            LEFT JOIN account_tax at ON at.id = aml.tax_line_id
            LEFT JOIN account_account_tag_account_move_line_rel aat_aml_rel ON aat_aml_rel.account_move_line_id = aml.id
            LEFT JOIN account_account_tag aat ON aat.id = aat_aml_rel.account_account_tag_id
            LEFT JOIN account_tax_report_line_tags_rel tag_rep_ln ON aat.id = tag_rep_ln.account_account_tag_id
            LEFT JOIN uom_uom uom ON uom.id = aml.product_uom_id
           WHERE aml.product_id IS NOT NULL AND am.state = 'posted'
        """
        return from_str

    def _group_by(sefl):
        group_by_str = """GROUP BY account_move_id,
            partner_id,
            product_id,
            date,
            journal_id,
            company_id,
            hsn_code,
            hsn_description
        """
        return group_by_str

    def init(self):
        tools.drop_view_if_exists(self.env.cr, self._table)
        self.env.cr.execute("""CREATE or REPLACE VIEW %s AS (
            %s
            FROM (
                %s %s
            ) AS sub %s)""" % (self._table, self._select(), self._sub_select(),
                               self._from(), self._group_by()))
