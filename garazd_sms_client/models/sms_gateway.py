# -*- coding: utf-8 -*-
# Copyright (C) 2015 Sébastien BEAU <sebastien.beau@akretion.com>
# Valentin CHEMIERE <valentin.chemiere@akretion.com>
# Copyright (C) 2018 Razumovskyi Yurii <GarazdCreation@gmail.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import api, models, fields

class SmsGateway(models.Model):
    _inherit = "sms.gateway"

    @api.multi
    def _provider_get_provider_conf(self, namespace):
        for rec in self:
            keychain = self.env['keychain.account']
            if rec._check_permissions():
                retrieve = keychain.suspend_security().retrieve
            else:
                retrieve = keychain.retrieve
            accounts = retrieve(
                [['namespace', '=', namespace]])
            return accounts[0]

    # def connect_to_server(self, namespace, params):
    #     """
    #         params: dictionary with additional values for SOAP connection
    #     """
    #     keychain_account = self._provider_get_provider_conf(ALPHASMS_KEYCHAIN_NAMESPACE)
    #     keychain_data = keychain_account.get_data()
    #     params['login'] = keychain_account['login']
    #     params['password'] = keychain_account._get_password()
    #     params['url'] = self.url
    #     # _logger.info("\n >>> params=%s", params)
    #     soap = Client(params['url'])
    #     return soap
    #
    # @api.multi
    # def test_server_connection(self):
    #     """
    #      Methods (3):
    #         checkbalance(Auth auth)
    #         send(Auth auth, Messages messages)
    #         status(Auth auth, MessagesStatus messages)
    #     """
    #     self.ensure_one()
    #     if self.method == 'soap_alphasms':
    #         keychain_account = self._provider_get_provider_conf(ALPHASMS_KEYCHAIN_NAMESPACE)
    #         keychain_data = keychain_account.get_data()
    #         params = {
    #             'login': keychain_account['login'],
    #             'password': keychain_account._get_password(),
    #             # 'url': self.url,
    #             'key': keychain_data['api_key'],
    #             }
    #         _logger.info("\n >>> params=%s", params)
    #         soap = Client('https://alphasms.ua/api/soap.php?wsdl') # params['url']
    #         _logger.info("\n >>> soap=%s", soap)
    #         auth_result = soap.service.checkbalance(params) #.encode('utf8')
    #         params.update({
    #             'password': '*****',
    #             'login': '*****',
    #             'api_key': '*****',
    #             })
    #         if auth_result:
    #             raise Warning('Success: %s' % auth_result)
    #         else:
    #             raise Warning('Authorization error: %s' % auth_result)
