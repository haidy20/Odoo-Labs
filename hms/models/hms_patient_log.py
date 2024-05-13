from odoo import models, fields, api

class HMSPatientLog(models.Model):
    _name = 'hms.patient.log'


    log_date = fields.Datetime(string='Log Date', default=fields.Datetime.now, required=True)
    log_content = fields.Text(string='Log Content', required=True)
    #patient_id = fields.Many2one(comodel_name='hms.patient', required=True)
    doctor_id = fields.Many2one(comodel_name='hms.doctor', required=True)