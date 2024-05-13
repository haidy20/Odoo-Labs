from odoo import fields, models


class Department(models.Model):
    _name = "hms.department"
    _rec_name = "name"
    name = fields.Char(string="Name" , required=True)
    capacity = fields.Integer(string="Capacity" , required=True)
    is_opened = fields.Boolean(string="Is Opened")
    patient_ids = fields.One2many(comodel_name="hms.patient",inverse_name="department_id", string="Patients")
