# coding: utf-8
# Copyright (C) 2015 Sébastien BEAU <sebastien.beau@akretion.com>
# Valentin CHEMIERE <valentin.chemiere@akretion.com>
# Copyright (C) 2017 Razumovskyi Yurii <GarazdCreation@gmail.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import api, models, fields
from ..models.keychain import TURBOSMS_KEYCHAIN_NAMESPACE
import logging
_logger = logging.getLogger(__name__)

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


class SmsSms(models.Model):
    _inherit = "sms.sms"

    turbosms_uuid = fields.Char('TurboSMS UUID')
    turbosms_state = fields.Char('TurboSMS Send State')

    @api.model
    def _prepare_soap_turbosms(self):
        keychain_account = self.gateway_id._provider_get_provider_conf()
        keychain_data = keychain_account.get_data()
        params = {
            'smsAccount': keychain_data['sms_account'],
            'login': keychain_account['login'],
            'password': keychain_account.get_password(),
            'from': self.gateway_id.from_provider,
            'url': self.gateway_id.url,
            'to': self._convert_to_e164(self.mobile),
            'message': self.message,
            }
        if self.nostop:
            params['noStop'] = 1
        if self.deferred:
            params['deferred'] = self.deferred
        if self.classes:
            params['class'] = self.classes
        if self.tag:
            params['tag'] = self.tag
        if self.coding:
            params['smsCoding'] = self.coding
        return params

    @api.model
    def _convert_to_e164(self, erp_number):
        to_dial_number = erp_number.replace(u'\xa0', u'')
        return to_dial_number

    @api.multi
    def _send_soap_turbosms(self):
        self.ensure_one()
        params = self._prepare_soap_turbosms()
        soap = Client(params['url'])
        auth_result = soap.service.Auth(params['login'],
                                        params['password']).encode('utf8')
        if auth_result != u'Вы успешно авторизировались':
            raise exceptions.Warning(u'Ошибка авторизации: %s' % auth_result)
        destination = self._convert_to_e164(self.mobile)
        message = self.message
        send_result = soap.service.SendSMS(params['smsAccount'],
                                params['to'], params['message']).ResultArray
        send_status = send_result[0].encode('utf8')
        self.turbosms_uuid = send_result[1].encode('utf8')
        params.update({
            'password': '*****',
            'to': '*****',
            'smsAccount': '*****',
            'login': '*****',
            })
        _logger.debug("\n Call TurboSMS API : %s params %s",
                      params['url'], params)
        if send_status != u'Сообщения успешно отправлены':
            raise ValueError(send_status)

    @api.multi
    def get_turbosms_send_status(self):
        self.ensure_one()
        if self.turbosms_uuid and self.gateway_id.method == 'soap_turbosms':
            keychain_account = self.gateway_id._provider_get_provider_conf()
            keychain_data = keychain_account.get_data()
            params = {
                'login': keychain_account['login'],
                'password': keychain_account.get_password(),
                'url': self.gateway_id.url,
                }
            soap = Client(params['url'])
            auth_result = soap.service.Auth(params['login'],
                                            params['password']).encode('utf8')
            params.update({
                'password': '*****',
                'login': '*****',
                })
            if auth_result != u'Вы успешно авторизировались':
                raise exceptions.Warning(u'Ошибка авторизации: %s' % auth_result)

            self.turbosms_state = soap.service.GetMessageStatus(self.turbosms_uuid)
