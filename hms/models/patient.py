from odoo import fields, models,api
from datetime import date
import re 
from odoo.exceptions import ValidationError

class Patient(models.Model):
    _name = "hms.patient"
    first_name = fields.Char(string="First Name", required=True)
    last_name = fields.Char(string="Last Name" , required=True)
    birth_date = fields.Date(string="Birth Date")
    history = fields.Html(string="History")
    cr_ratio = fields.Float(string="CR Ratio")
    blood_group = fields.Selection([
        ('a+', 'A+'),('a-', 'A-'), ('b+', 'B+'),('b-', 'B-'),
        ('o+', 'O+'),('o-', 'O-'),('ab+', 'AB+'), ('ab-', 'AB-'),
    ], string="Blood Type")
    pcr_test = fields.Boolean(string="PCR Test")
    image = fields.Image(string="Image")
    address = fields.Text(string="Address")
    birth_date = fields.Date()
    age = fields.Integer(string='Age', compute='_compute_age', store=True)

    department_id = fields.Many2one(comodel_name="hms.department", string="Department")
    doctor_ids = fields.Many2many(comodel_name="hms.doctor")
    department_capacity = fields.Integer(string="Department Capacity", related="department_id.capacity")
    state = fields.Selection([
        ('undetermined', 'Undetermined'),
        ('good', 'Good'),('fair', 'Fair'),('serious', 'Serious'),
    ], string="State", default='undetermined')

    email = fields.Char(string='Email', required=True, unique=True)
    
    _sql_constraints = [
        ('unique_email', 'unique(email)', ' Email address must be unique.'),
    ]

    @api.onchange('age')
    def _onchange_age(self):
        if self.age:
            if self.age < 30:
                self.pcr_test = True
                return {
                    "warning": {
                        "title": "Warning massages",
                        "message": "PCR is checked by default for patients less than 30 years old",
                    }
                }
            else:
                self.pcr_test = False

    @api.depends('birth_date')
    def _compute_age(self):
        for rec in self:
            if rec.birth_date:
                today = date.today()
                birth_date = rec.birth_date
                age = today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))
                rec.age = age
            else:
                rec.age = 1

    def states(self):
        if self.state == "undetermined":
            self.state = "good"
        elif self.state == "good":
            self.state = "fair"
        elif self.state == "fair":
            self.state = "serious"
        else:
            self.state = "undetermined"


    @api.onchange('email')
    def validate_mail(self):
        if self.email:
            match = re.match('^[_a-z0-9-]+(\.[_a-z0-9-]+)*@[a-z0-9-]+(\.[a-z0-9-]+)*(\.[a-z]{2,4})$', self.email)
            if match == None:
                raise ValidationError('Not a valid E-mail ID')


