# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError

class account_payment(models.Model):
    _inherit = 'account.payment'

    tds = fields.Boolean(string='TDS', default=False, readonly=True, states={'draft': [('readonly', False)]}, tracking=True)
    challan_no = fields.Char(string='Challan Serial No', readonly=True, states={'draft': [('readonly', False)]}, tracking=True)
    tds_section_id = fields.Many2one('tds.section', string='Section', readonly=True, states={'draft': [('readonly', False)]}, tracking=True)
    bsr_code = fields.Char(sring='BSR Code', readonly=True, states={'draft': [('readonly', False)]}, tracking=True)
    reference_no = fields.Char(sring='Ref No.', readonly=True, states={'draft': [('readonly', False)]}, tracking=True)
    account_account_id = fields.Many2one('account.account', string='Account', domain="[('tds_account', '=', True), ('company_id', '=', company_id)]",
                                         readonly=True, states={'draft': [('readonly', False)]}, tracking=True)

    # def _prepare_payment_moves(self):
    #     all_move_vals = []
    #     for payment in self:
    #         if payment.tds:
    #             pass
    #         else:
    #             res = super(account_payment, self)._prepare_payment_moves()
    #             return res

    @api.depends('invoice_ids', 'payment_type', 'partner_type', 'partner_id', 'tds')
    def _compute_destination_account_id(self):
        self.destination_account_id = False
        for payment in self:
            if payment.tds:
                payment.destination_account_id = payment.account_account_id.id
            else:
                super(account_payment, self)._compute_destination_account_id()





