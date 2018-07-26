# -*- coding: utf-8 -*-

from odoo import api, fields, models

class CrmLead(models.Model):
    _inherit = "crm.lead"

    sms_qty = fields.Integer('SMS', compute="_count_lead_sms", store=False)
    sms_opt_out = fields.Boolean('SMS Opt-out')
    viber_on_phone = fields.Boolean('Viber on Phone')
    viber_on_mobile = fields.Boolean('Viber on Mobile')

    @api.depends('name')
    def _count_lead_sms(self):
        for record in self:
            record.sms_qty = len(self.env['sms.sms'].search([('lead_id', '=', record.id)]))
