# -*- coding: utf-8 -*-

from odoo import models, fields, api


class ResPartner(models.Model):
    _inherit = 'res.partner'

    pan_number = fields.Char(string='PAN Number')


class TdsSection(models.Model):
    _name = 'tds.section'
    _description = 'TDS Section'

    name = fields.Char(string='Section Name')
    percentage = fields.Integer(string='Percentage', default=0)


class AccountAccount(models.Model):
    _inherit = 'account.account'

    tds_account = fields.Boolean(string='TDS', default=False)





