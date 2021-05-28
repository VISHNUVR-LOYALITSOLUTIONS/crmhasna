# -*- coding: utf-8 -*-

from odoo.tools import DEFAULT_SERVER_DATE_FORMAT
from odoo import models, fields, api
from io import BytesIO
import xlwt
from datetime import datetime
import base64


class TdsReportWizard(models.TransientModel):
    _name = 'tds.report.wizard'

    date_from = fields.Date('Date From', required=True, default=fields.Date.context_today)
    date_to = fields.Date('Date To', required=True, default=fields.Date.context_today)
    state = fields.Selection([('choose', 'choose'), ('get', 'get')],
                             default='choose')

    company_id = fields.Many2one('res.company', string='Company', required=True,
                                 default=lambda self: self.env['res.company']._company_default_get(
                                     'tds.report.wizard'))

    report = fields.Binary('Prepared file', filters='.xls', readonly=True)
    name = fields.Char('File Name', size=128)
    sorted_payments = []

    def get_valid_payments(self):
        # Searching for tds payments
        from_date = datetime.strptime(str(self.date_from), '%Y-%m-%d').date()
        to_date = datetime.strptime(str(self.date_to), '%Y-%m-%d').date()
        company_id = self.company_id.id

        # Get all tds payments
        payments = self.env['account.payment'].search([('payment_date', '>=', from_date),
            ('payment_date', '<=', to_date), ('state', 'not in', ['draft', 'cancelled']),
                                                       ('tds', '=', True), ('company_id', '=', company_id)])
        self.sorted_payments = payments.sorted(key=lambda p: p.payment_date)

    def generate_tds_report(self):
        self.ensure_one()
        fp = BytesIO()
        xl_workbook = xlwt.Workbook(encoding='utf-8')
        from_date = datetime.strptime(str(self.date_from), '%Y-%m-%d').date()
        to_date = datetime.strptime(str(self.date_to), '%Y-%m-%d').date()
        # Get the invoices
        self.get_valid_payments()
        self.generate_tds_collection_report(xl_workbook)
        xl_workbook.save(fp)
        out = base64.encodestring(fp.getvalue())
        self.write({'state': 'get',
                    'report': out,
                    'name': 'TDS' + str(from_date) + '-' + str(to_date) + '.xls'
                    })
        return {
            'type': 'ir.actions.act_window',
            'res_model': 'tds.report.wizard',
            'view_mode': 'form',
            'view_type': 'form',
            'res_id': self.id,
            'views': [(False, 'form')],
            'target': 'new',
        }

    def category_tsd_report(self):
        from_date = datetime.strptime(str(self.date_from), '%Y-%m-%d').date()
        to_date = datetime.strptime(str(self.date_to), '%Y-%m-%d').date()
        company_id = self.company_id.id
        lines = []
        res = {}
        coa = {}
        for payment in self.sorted_payments:
            taxable_amount = 0
            deducted_date = ""
            reconciled_moves = payment.move_line_ids.mapped('matched_debit_ids.debit_move_id.move_id') \
                               + payment.move_line_ids.mapped('matched_credit_ids.credit_move_id.move_id')
            for moves in reconciled_moves:
                taxable_amount += sum(moves.line_ids.mapped('credit'))
                deducted_date = moves.date

            res = {
                'challan_no': payment.challan_no,
                'deductee_name': payment.partner_id.name,
                'pan_no': payment.partner_id.pan_number,
                'deducted_month': datetime.strptime(str(deducted_date), '%Y-%m-%d').strftime("%b'%Y") if deducted_date else " ",
                'deducted_date': datetime.strptime(str(deducted_date), '%Y-%m-%d').strftime('%d-%m-%Y') if deducted_date else " ",
                'paid_date': datetime.strptime(str(payment.payment_date), '%Y-%m-%d').strftime('%d-%m-%Y') if payment.payment_date else " ",
                'taxable_amount': taxable_amount,
                'tds': payment.amount,
                'rate': payment.tds_section_id.percentage,
                'section': payment.tds_section_id.name,
                'bank_branch': payment.journal_id.bank_id.name if payment.journal_id.bank_id else " ",
                'bsr_code': payment.bsr_code,
                'ref_no': payment.reference_no,
            }
            if payment.account_account_id.code in coa:
                coa[payment.account_account_id.code].append(res)
            else:
                coa[payment.account_account_id.code] = [res]
        return coa

    def generate_tds_collection_report(self, wb1):
        self.ensure_one()
        ws1 = wb1.add_sheet('TDS REPORT')
        fp = BytesIO()
        # Content/Text style
        header_content_style = xlwt.easyxf("font: name Calibri;font: bold 1, height 230; align: horiz center")
        sub_header_style = xlwt.easyxf("font: name Calibri; font: height 230; align: horiz center")
        line_header_bold_style = xlwt.easyxf("font: name Calibri; font: bold 1, height 210; align: horiz center")
        line_header_bold_right_style = xlwt.easyxf("font: name Calibri; font: bold 1, height 210; align: horiz right")
        line_header_style = xlwt.easyxf("font: name Calibri; font: height 210; align: horiz center")

        ws1.col(0).width = 8000
        ws1.col(1).width = 8200
        ws1.col(2).width = 7500
        ws1.col(3).width = 7500
        ws1.col(4).width = 7500
        ws1.col(5).width = 7500
        ws1.col(6).width = 7500
        ws1.col(7).width = 7500
        ws1.col(8).width = 7500
        ws1.col(9).width = 7500
        ws1.col(10).width = 7500
        ws1.col(11).width = 7500
        ws1.col(12).width = 7500

        row = 0
        col = -1
        ws1.row(row).height = 500
        ws1.write_merge(row, row, col+1, col + 13, self.company_id.name, header_content_style)
        row += 1
        result = self.category_tsd_report()
        for key in result:
            coa = self.env['account.account'].search([('code', '=', key)])
            coa_name = coa.name if coa else " "
            taxable_amount = 0
            tds = 0
            ws1.row(row).height = 500
            ws1.write_merge(row, row, col+1, col + 13, "TDS COLLECTION FOR(" + coa_name + ")", sub_header_style)
            row += 1
            ws1.write(row, col + 1, "Challan Serial No", line_header_bold_style)
            ws1.write(row, col + 2, "Deductee Name", line_header_style)
            ws1.write(row, col + 3, "PAN Number", line_header_style)
            ws1.write(row, col + 4, "Deducted Month", line_header_style)
            ws1.write(row, col + 5, "Deducted Date", line_header_style)
            ws1.write(row, col + 6, "Paid Date", line_header_bold_style)
            ws1.write(row, col + 7, "Taxable amount", line_header_style)
            ws1.write(row, col + 8, "Tds", line_header_bold_style)
            ws1.write(row, col + 9, "Rate", line_header_style)
            ws1.write(row, col + 10, "Section", line_header_style)
            ws1.write(row, col + 11, "Bank Branch", line_header_style)
            ws1.write(row, col + 12, "BSR CODE", line_header_style)
            ws1.write(row, col + 13, "Ref No.", line_header_bold_style)
            row += 1
            for line in result[key]:
                taxable_amount += line['taxable_amount']
                tds += line['tds']
                ws1.write(row, col + 1, line['challan_no'], line_header_bold_style)
                ws1.write(row, col + 2, line['deductee_name'], line_header_style)
                ws1.write(row, col + 3, line['pan_no'], line_header_style)
                ws1.write(row, col + 4, line['deducted_month'], line_header_style)
                ws1.write(row, col + 5, line['deducted_date'], line_header_style)
                ws1.write(row, col + 6, line['paid_date'], line_header_style)
                ws1.write(row, col + 7, line['taxable_amount'], line_header_bold_right_style)
                ws1.write(row, col + 8, line['tds'], line_header_style)
                ws1.write(row, col + 9, line['rate'], line_header_bold_style)
                ws1.write(row, col + 10, line['section'], line_header_style)
                ws1.write(row, col + 11, line['bank_branch'], line_header_style)
                ws1.write(row, col + 12, line['bsr_code'], line_header_style)
                ws1.write(row, col + 13, line['ref_no'], line_header_style)
                row += 1
            ws1.write(row, col + 1, " ", line_header_bold_style)
            ws1.write(row, col + 2, " ", line_header_style)
            ws1.write(row, col + 3, " ", line_header_style)
            ws1.write(row, col + 4, " ", line_header_style)
            ws1.write(row, col + 5, " ", line_header_style)
            ws1.write(row, col + 6, " ", line_header_style)
            ws1.write(row, col + 7, taxable_amount, line_header_bold_style)
            ws1.write(row, col + 8, tds, line_header_style)
            ws1.write(row, col + 9, " ", line_header_bold_style)
            ws1.write(row, col + 10, " ", line_header_style)
            ws1.write(row, col + 11, " ", line_header_style)
            ws1.write(row, col + 12, " ", line_header_style)
            ws1.write(row, col + 13, " ", line_header_style)
            row += 1


    def format_date(self, date_in):
        return datetime.strftime(datetime.strptime(str(date_in), DEFAULT_SERVER_DATE_FORMAT), "%d/%m/%Y")

