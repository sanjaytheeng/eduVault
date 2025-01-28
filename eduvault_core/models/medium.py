from odoo import models, fields, api, _

class OpMedium(models.Model):
    _name = "op.medium"
    _description = "eduvault mediums"

    name = fields.Char('Name')