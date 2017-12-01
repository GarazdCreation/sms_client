# coding: utf-8
# Copyright (C) 2017 Razumovskyi Yurii <GarazdCreation@gmail.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import models, fields, api, _
from openerp.exceptions import Warning
from suds.client import Client


class WizardMassSms(models.TransientModel):
    _inherit = 'wizard.mass.sms'

    balance = fields.Char('SMS balance', store=False,
                          compute='_compute_sms_balance')
    char_qty = fields.Integer('Qty of characters', store=True,
                                compute='_compute_message_characters')

    @api.one
    @api.depends('message')
    def _compute_message_characters(self):
        if self.message:
            self.char_qty = len(self.message)

    @api.one
    @api.depends('gateway_id')
    def _compute_sms_balance(self):
        if self.gateway_id.method == 'soap_turbosms':
            keychain_account = self.gateway_id._provider_get_provider_conf()
            keychain_data = keychain_account.get_data()
            params = {
                'login': keychain_account['login'],
                'password': keychain_account.get_password(),
                'url': self.gateway_id.url,
                }
            soap = Client(params['url'])
            auth_result = soap.service.Auth(
                params['login'],
                params['password']).encode('utf8'
            )
            params.update({
                'password': '*****',
                'login': '*****',
                })

            if auth_result != u'Вы успешно авторизировались':
                raise Warning(_(u'Ошибка авторизации: %s' % auth_result))
            else:
                self.balance = soap.service.GetCreditBalance()

    @api.model
    def _prepare_sms_vals(self, partner):
        """
        Rewrite method: insert phone or mobile or fax in field 'mobile'
        """
        sms_to_phone = partner.phone
        if not sms_to_phone:
            sms_to_phone = partner.mobile
        if not sms_to_phone:
            sms_to_phone = partner.fax
        if not sms_to_phone:
            raise Warning(_("The partner %s does not have a phone number." % partner.name))

        return {
            'gateway_id': self.gateway_id.id,
            'company_id': self.env.user.company_id.id,
            'state': 'draft',
            'message': self.message,
            'validity': self.validity,
            'classes': self.classes,
            'deferred': self.deferred,
            'priority': self.priority,
            'coding': self.coding,
            'tag': self.tag,
            'nostop': self.nostop,
            'partner_id': partner.id,
            'mobile': sms_to_phone,
        }

    @api.multi
    def send(self):
        sms_obj = self.env['sms.sms']
        partner_obj = self.env['res.partner']
        for partner in partner_obj.browse(self._context.get('active_ids')):
            if not partner.sms_opt_out:
                vals = self._prepare_sms_vals(partner)
                sms_obj.create(vals)
