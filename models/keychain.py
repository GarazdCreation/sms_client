# coding: utf-8
# Copyright (C) 2015 Sébastien BEAU <sebastien.beau@akretion.com>
# Valentin CHEMIERE <valentin.chemiere@akretion.com>
# Copyright (C) 2017 Razumovskyi Yurii <GarazdCreation@gmail.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import models, fields

TURBOSMS_KEYCHAIN_NAMESPACE = 'turbosms_provider'


class Keychain(models.Model):
    _inherit = 'keychain.account'

    namespace = fields.Selection(
        selection_add=[(TURBOSMS_KEYCHAIN_NAMESPACE, 'TurboSMS')])

    def _turbosms_provider_init_data(self):
        return {'sms_account': ""}

    def _turbosms_provider_validate_data(self, data):
        return True
