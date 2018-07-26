# -*- coding: utf-8 -*-
# Copyright (C) 2018 Razumovskyi Yurii <GarazdCreation@gmail.com>

from odoo import api, fields, models

class SmsSms(models.Model):
    _inherit = "sms.sms"

    lead_id = fields.Many2one(
        'crm.lead',
        readonly=True,
        states={'draft': [('readonly', False)]},
        string='Lead')

    @api.onchange('lead_id')
    def onchange_lead_id(self):
        self.mobile = self.lead_id.mobile
