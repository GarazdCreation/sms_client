# -*- coding: utf-8
# Copyright (C) 2018 Razumovskyi Yurii <GarazdCreation@gmail.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import models, fields, api, _
from odoo.exceptions import Warning

class WizardMassSms(models.TransientModel):
    _inherit = 'wizard.mass.sms'

    model_name = fields.Selection([('partner','Partners'),('lead','Leads')], string="Recipients", default='partner')
    balance = fields.Char('Balance', store=False,
                          compute='_compute_sms_balance')
    char_qty = fields.Integer('Characters', store=True, readonly=True,
                              compute='_compute_message_characters')
    channel = fields.Selection([('sms','SMS'),('viber','Viber')],
                               string="Channel", default='sms', required=True)
    media_type = fields.Selection([('text', 'Text'), ('image', 'Only Image w/o Text'), ('button', 'Button')], default='text')
    media_image = fields.Char('Image URL', help="Extensions for image: jpg, jpeg, png or gif.")
    media_button = fields.Char('Button Text', size=19)
    media_url = fields.Char('URL')
    partners_count = fields.Integer('Recipients Count', compute='_compute_partners_count')
    partner_customer = fields.Boolean('Customers', default=True)
    partner_supplier = fields.Boolean('Suppliers')
    partner_viber = fields.Boolean('With Viber')

    @api.depends('gateway_id')
    def _compute_sms_balance(self):
        pass

    @api.depends('message')
    def _compute_message_characters(self):
        for record in self:
            if record.message:
                record.char_qty = len(record.message)

    @api.depends('partner_ids')
    def _compute_partners_count(self):
        for record in self:
            record.partners_count = len(record.partner_ids)

    @api.multi
    def action_partner_search(self):
        for record in self:
            vals = []
            if record.partner_viber:
                vals.append('|')
                vals.append(('viber_on_phone','=',True))
                vals.append(('viber_on_mobile','=',True))
            if record.partner_customer:
                vals.append(('customer','=',True))
            if record.partner_supplier:
                vals.append(('supplier','=',True))
            partners = self.env['res.partner'].search(vals).mapped('id')
            record.update({'partner_ids': [(6, 0, partners)]})
            return {
                'type': 'ir.actions.act_window',
                'name': _('Send message'),
                'res_model': record._name,
                'res_id': record.id,
                'view_type': 'form',
                'view_mode': 'form',
                'target': 'new',
            }

    @api.model
    def _prepare_sms_vals(self, partner):
        """
        Rewrite method: insert phone or mobile or fax in field 'mobile'
        """
        to_phone = ''
        if self.channel == 'sms':
            to_phone = partner.mobile or partner.phone or partner.fax
            # if not sms_to_phone:
            #     sms_to_phone = partner.mobile
            # if not sms_to_phone:
            #     sms_to_phone = partner.fax
            if not to_phone:
                raise Warning(_("The partner %s does not have a phone number." % partner.name))
        elif self.channel == 'viber':
            viber_phone = ''
            if partner.viber_on_mobile and partner.mobile:
                viber_phone = partner.mobile
            elif partner.viber_on_phone and partner.phone:
                viber_phone = partner.phone
            to_phone = viber_phone
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
            'mobile': to_phone,
            'channel': self.channel,
            'media_type': self.media_type,
            'media_image': self.media_image,
            'media_button': self.media_button,
            'media_url': self.media_url,
        }

    @api.multi
    def send(self):
        sms_obj = self.env['sms.sms']
        partner_obj = self.env['res.partner']
        for partner in partner_obj.browse(self._context.get('active_ids')):
            if self.channel == 'sms' and not partner.sms_opt_out or self.channel == 'viber' and (partner.viber_on_phone or partner.viber_on_mobile):
                vals = self._prepare_sms_vals(partner)
                sms_obj.create(vals)
