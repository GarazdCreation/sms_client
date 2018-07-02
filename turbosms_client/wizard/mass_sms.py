# coding: utf-8
# Copyright (C) 2017 Razumovskyi Yurii <GarazdCreation@gmail.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from suds.client import Client
from odoo import models, fields, api, _
from odoo.exceptions import Warning
from ..models.keychain import TURBOSMS_KEYCHAIN_NAMESPACE

class WizardMassSms(models.TransientModel):
    _inherit = 'wizard.mass.sms'

    # balance_turbosms = fields.Char('SMS balance', store=False,
    #                       compute='_compute_turbosms_balance')

    @api.depends('gateway_id')
    def _compute_sms_balance(self):
        for record in self:
            rec = super(WizardMassSms, record)._compute_sms_balance()
            if record.gateway_id.method == 'soap_turbosms':
                keychain_account = record.gateway_id._provider_get_provider_conf(TURBOSMS_KEYCHAIN_NAMESPACE)
                keychain_data = keychain_account.get_data()
                params = {
                    'login': keychain_account['login'],
                    'password': keychain_account._get_password(),
                    'url': record.gateway_id.url,
                    }
                soap = Client(params['url'])
                auth_result = soap.service.Auth(params['login'], params['password']).encode('utf8')
                params.update({
                    'password': '*****',
                    'login': '*****',
                    })
                if auth_result != 'Вы успешно авторизировались':
                    raise Warning(_('Authorization error: %s' % auth_result))
                else:
                    record.balance = soap.service.GetCreditBalance()
            return rec
