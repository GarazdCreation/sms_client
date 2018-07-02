# coding: utf-8
# Copyright (C) 2015 Sébastien BEAU <sebastien.beau@akretion.com>
# Valentin CHEMIERE <valentin.chemiere@akretion.com>
# Copyright (C) 2017 Razumovskyi Yurii <GarazdCreation@gmail.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import api, models, fields, _
from odoo.exceptions import Warning
from ..models.keychain import TURBOSMS_KEYCHAIN_NAMESPACE
import logging
_logger = logging.getLogger(__name__)

try:
    from suds.client import Client
except :
    _logger.warning("ERROR IMPORTING suds, if not installed, please install it:"
    " e.g.: apt-get install python-suds")


class SmsSms(models.Model):
    _inherit = "sms.sms"

    # company_id = fields.Many2one(default=lambda self: self.env.user.company_id.id)
    turbosms_uuid = fields.Char('TurboSMS UUID', deprecated=True)
    turbosms_state = fields.Char('TurboSMS Send State', deprecated=True)

    @api.model
    def _prepare_soap_turbosms(self):
        keychain_account = self.gateway_id._provider_get_provider_conf(TURBOSMS_KEYCHAIN_NAMESPACE)
        try:
            keychain_data = keychain_account.get_data()
            smsAccount = keychain_data['sms_account']
        except:
            raise KeyError(_("Specify the sender's name in the Keychain settings in the format: {'sms_account': 'sender_name'}"))
        params = {
            'smsAccount': smsAccount,
            'login': keychain_account['login'],
            'password': keychain_account._get_password(),
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

    @api.multi
    def _send_soap_turbosms(self):
        self.ensure_one()
        params = self._prepare_soap_turbosms()
        soap = Client(params['url'])
        auth_result = soap.service.Auth(params['login'],
                                        params['password']).encode('utf8')
        if auth_result != 'Вы успешно авторизировались':
            raise Warning('Authorization error: %s' % auth_result)
        destination = self._convert_to_e164(self.mobile)
        message = self.message
        send_result = soap.service.SendSMS(params['smsAccount'],
                                params['to'], params['message']).ResultArray
        _logger.debug("\n TurboSMS send_result:  %s", send_result)
        send_status = send_result[0].encode('utf8')
        if send_status != 'Сообщения успешно отправлены':
            raise ValueError(send_status)
        self.provider_uuid = send_result[1].encode('utf8')
        params.update({
            'password': '*****',
            'to': '*****',
            'smsAccount': '*****',
            'login': '*****',
            })
        _logger.debug("\n Call TurboSMS API : %s params %s",
                      params['url'], params)

    @api.multi
    def get_sms_send_status(self):
        self.ensure_one()
        rec = super(SmsSms, self).get_sms_send_status()
        if self.provider_uuid and self.gateway_id.method == 'soap_turbosms':
            keychain_account = self.gateway_id._provider_get_provider_conf(TURBOSMS_KEYCHAIN_NAMESPACE)
            keychain_data = keychain_account.get_data()
            params = {
                'login': keychain_account['login'],
                'password': keychain_account._get_password(),
                'url': self.gateway_id.url,
                }
            soap = Client(params['url'])
            auth_result = soap.service.Auth(params['login'],
                                            params['password']).encode('utf8')
            params.update({
                'password': '*****',
                'login': '*****',
                })
            if auth_result != 'Вы успешно авторизировались':
                raise Warning('Authorization error: %s' % auth_result)
            self.provider_state = soap.service.GetMessageStatus(self.provider_uuid)
        return rec
