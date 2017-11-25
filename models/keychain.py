# coding: utf-8
# Copyright (C) 2015 Sébastien BEAU <sebastien.beau@akretion.com>
# Valentin CHEMIERE <valentin.chemiere@akretion.com>
# Copyright (C) 2017 Razumovskyi Yurii <GarazdCreation@gmail.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import models, fields, api

TURBOSMS_KEYCHAIN_NAMESPACE = 'turbosms_provider'


class Keychain(models.Model):
    _inherit = 'keychain.account'

    namespace = fields.Selection(
        selection_add=[(TURBOSMS_KEYCHAIN_NAMESPACE, 'TurboSMS')])

    def _turbosms_provider_init_data(self):
        return {'sms_account': ""}

    def _turbosms_provider_validate_data(self, data):
        return True

class Partner(models.Model):
    _inherit = "res.partner"
    sms_qty = fields.Integer('SMS', compute="_count_partner_sms", store=False)
    sms_opt_out = fields.Boolean('Opt Out from SMS')

    @api.one
    @api.depends('name')
    def _count_partner_sms(self):
        self.sms_qty = len(self.env['sms.sms'].search([('partner_id', '=', self.id)]))
