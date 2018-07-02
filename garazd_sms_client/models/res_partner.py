# coding: utf-8
# Copyright (C) 2017 Razumovskyi Yurii <GarazdCreation@gmail.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import models, fields, api

class Partner(models.Model):
    _inherit = "res.partner"

    sms_qty = fields.Integer('SMS', compute="_count_partner_sms", store=False)
    sms_opt_out = fields.Boolean('SMS Opt-out')
    viber_on_phone = fields.Boolean('Viber on Phone')
    viber_on_mobile = fields.Boolean('Viber on Mobile')

    @api.depends('name')
    def _count_partner_sms(self):
        for record in self:
            record.sms_qty = len(self.env['sms.sms'].search([('partner_id', '=', record.id)]))
