# coding: utf-8
# Copyright (C) 2015 Sébastien BEAU <sebastien.beau@akretion.com>
# Valentin CHEMIERE <valentin.chemiere@akretion.com>
# Copyright (C) 2017 Razumovskyi Yurii <GarazdCreation@gmail.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import api, models, fields
from odoo.exceptions import Warning
from ..models.keychain import TURBOSMS_KEYCHAIN_NAMESPACE

try:
    from suds.client import Client
except :
    _logger.warning("ERROR IMPORTING suds, if not installed, please install it:"
    " e.g.: apt-get install python-suds")


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

    @api.multi
    def test_turbosms_connection(self):
        self.ensure_one()
        if self.method == 'soap_turbosms':
            keychain_account = self._provider_get_provider_conf()
            keychain_data = keychain_account.get_data()
            params = {
                'login': keychain_account['login'],
                'password': keychain_account._get_password(),
                'url': self.url,
                }
            soap = Client(params['url'])
            auth_result = soap.service.Auth(params['login'],
                                            params['password']).encode('utf8')
            params.update({
                'password': '*****',
                'login': '*****',
                })
            if auth_result == 'Вы успешно авторизировались':
                raise Warning('Success: %s' % auth_result)
            else:
                raise Warning('Authorization error: %s' % auth_result)
