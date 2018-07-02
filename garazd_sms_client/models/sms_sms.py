# -*- coding: utf-8 -*-
# Copyright (C) 2018 Razumovskyi Yurii <GarazdCreation@gmail.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import api, models, fields

class SmsSms(models.Model):
    _inherit = "sms.sms"

    company_id = fields.Many2one(default=lambda self: self.env.user.company_id.id)
    message = fields.Text(size=1000)
    provider_uuid = fields.Char('Provider UUID', readonly=True)
    provider_state = fields.Char('Provider Send State', readonly=True)
    sms_count = fields.Integer('SMS Count', readonly=True)
    char_qty = fields.Integer('Characters', store=True, readonly=True,
        compute='_compute_message_characters')
    channel = fields.Selection([
            ('sms','SMS'),
            ('viber','Viber'),
        ], string='Channel', default='sms', required=True)
    media_type = fields.Selection([
            ('text', 'Text'),
            ('image', 'Only Image w/o Text'),
            ('button', 'Button'),
        ], string='Media Type', default='text')
    media_image = fields.Char('Image URL', help="Extensions for image: jpg, jpeg, png or gif.")
    media_button = fields.Char('Button Text', size=19)
    media_url = fields.Char('URL')

    @api.model
    def _convert_to_e164(self, erp_number):
        to_dial_number = erp_number.replace(u'\xa0', u'')
        return to_dial_number

    @api.multi
    def get_sms_send_status(self):
        pass

    @api.depends('message')
    def _compute_message_characters(self):
        for record in self:
            if record.message:
                record.char_qty = len(record.message)
