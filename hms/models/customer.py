from odoo import models, fields,api
from odoo.exceptions import ValidationError
from datetime import date


class Customer(models.Model):
    _inherit = 'res.partner'
    vat = fields.Char(required=True)
    related_patient_id = fields.Many2one(comodel_name='hms.patient', string='Related Patient')
   


    @api.constrains('related_patient_id')
    def _check_unique_related_patient_id(self):
        for customer in self:
            if customer.related_patient_id:
                existing_customer = self.env['res.partner'].search([
                    ('related_patient_id', '=', customer.related_patient_id.id),
                    ('id', '!=', customer.id)
                ], limit=1)
                if existing_customer:
                    raise ValidationError('This patient is already linked to another customer.')
                