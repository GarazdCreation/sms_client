# coding: utf-8
# Copyright (C) 2015 Sébastien BEAU <sebastien.beau@akretion.com>
# Valentin CHEMIERE <valentin.chemiere@akretion.com>
# Copyright (C) 2017 Razumovskyi Yurii <GarazdCreation@gmail.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import api, models, fields
from ..models.keychain import TURBOSMS_KEYCHAIN_NAMESPACE


class SmsClient(models.Model):
    _inherit = "sms.gateway"

    method = fields.Selection(selection_add=[('soap_turbosms', 'TurboSMS SOAP')])

    @api.multi
    def _provider_get_provider_conf(self):
        for rec in self:
            keychain = rec.env['keychain.account']
            if rec._check_permissions():
                retrieve = keychain.suspend_security().retrieve
            else:
                retrieve = keychain.retrieve
            accounts = retrieve(
                [['namespace', '=', TURBOSMS_KEYCHAIN_NAMESPACE]])
            return accounts[0]
