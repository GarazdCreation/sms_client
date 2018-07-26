# -*- coding: utf-8
# Copyright (C) 2018 Razumovskyi Yurii <GarazdCreation@gmail.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import models, fields, api, _
from odoo.exceptions import Warning

class WizardMassSms(models.TransientModel):
    _inherit = "wizard.mass.sms"

    @api.model
    def _default_get_lead(self):
        if self._context.get('active_model') == 'crm.lead':
            return self._context.get('active_ids')

    lead_ids = fields.Many2many('crm.lead', default=_default_get_lead)
    stage_id = fields.Many2one('crm.stage', 'Lead Stage')
    tag_ids = fields.Many2many('crm.lead.tag', string='Tags')

    @api.depends('partner_ids', 'lead_ids')
    def _compute_partners_count(self):
        for record in self:
            count = len(record.partner_ids)
            count += len(record.lead_ids)
            record.partners_count = count

    @api.multi
    def action_lead_search(self):
        for record in self:
            vals = []
            if record.partner_viber:
                vals.append('|')
                vals.append(('viber_on_phone','=',True))
                vals.append(('viber_on_mobile','=',True))
            if record.tag_ids:
                vals.append(('tag_ids','in',record.tag_ids.mapped('id')))
            if record.stage_id:
                vals.append(('stage_id','=',record.stage_id.id))
            leads = self.env['crm.lead'].search(vals).mapped('id')
            record.update({'lead_ids': [(6, 0, leads)]})
            return {
                'type': 'ir.actions.act_window',
                'name': _('Send message'),
                'res_model': record._name,
                'res_id': record.id,
                'view_type': 'form',
                'view_mode': 'form',
                'target': 'new',
            }

    @api.multi
    def send(self):
        if self._context.get('active_model') == 'crm.lead':
            sms_obj = self.env['sms.sms']
            lead_obj = self.env['crm.lead']
            for lead in lead_obj.browse(self._context.get('active_ids')):
                if self.channel == 'sms' and not lead.sms_opt_out or self.channel == 'viber' and (lead.viber_on_phone or lead.viber_on_mobile):
                    vals = self._prepare_sms_vals(lead)
                    vals['lead_id'] = lead.id
                    vals['partner_id'] = None
                    sms_obj.create(vals)
        else:
            rec = super(WizardMassSms, self).send()
            return rec
