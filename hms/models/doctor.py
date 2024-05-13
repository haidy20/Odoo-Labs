from odoo import fields, models


class Doctors(models.Model):
    _name = "hms.doctor"
    _rec_name = "first_name"
    first_name = fields.Char(string="First Name", required=True)
    last_name = fields.Char(string="Last Name", required=True)
    image = fields.Image(string="Image")
