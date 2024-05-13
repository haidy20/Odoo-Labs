from odoo import models, fields,api
from odoo.exceptions import ValidationError
import re
from datetime import date


class HMSPatient(models.Model):

    _name = 'hms.patient'
    _rec_name = "first_name"

    first_name = fields.Char(string='First Name', required=True)
    last_name = fields.Char(string='Last Name', required=True)
    email = fields.Char(string='Email', required=True)

    birth_date = fields.Date(string='Birth Date')
    history = fields.Html(string='History')
    cr_ratio = fields.Float(string='CR Ratio')
    blood_type = fields.Selection([('A', 'A'), ('B', 'B'), ('AB', 'AB'), ('O', 'O')],string='Blood Type')
    pcr = fields.Boolean(string='PCR')
    image = fields.Binary(string='Image')
    address = fields.Text(string='Address')

    age=fields.Integer(string='Age',compute='_compute_age', store=True, readonly=True)

    department_id = fields.Many2one(comodel_name='hms.department')
    doctor_ids = fields.Many2many(comodel_name='hms.doctor')
    department_capacity = fields.Integer(related='department_id.capacity')
    #log_ids = fields.One2many(comodel_name='hms.patient.log', inverse_name='patient_id')
    state = fields.Selection([
        ('undetermined', 'Undetermined'),
        ('good', 'Good'),
        ('fair', 'Fair'),
        ('serious', 'Serious')
    ], string='State', default='undetermined')
    
    
    @api.onchange('age')
    def onchange_age(self):
        if self.age < 30:
            self.pcr = True
            return {'warning': {'title': 'Warning', 'message': 'PCR is required for patients under 30 years old'}}
        
    
    @api.constrains('email')
    def _check_valid_email(self):
        for record in self:
            if record.email:
                if not re.match(r'^[\w\.-]+@[\w\.-]+\.\w+$', record.email):
                    raise ValidationError("Invalid email address. Please enter a valid email.")

    @api.depends('birth_date')
    def _compute_age(self):
        today = date.today()
        for patient in self:
            if patient.birth_date:
                delta = today.year - patient.birth_date.year - ((today.month, today.day) < (patient.birth_date.month, patient.birth_date.day))
                patient.age = delta
            else:
                patient.age = 0
                

    _sql_constraints = [
        ('unique_email', 'UNIQUE(email)', 'Email must be unique.')
    ]



