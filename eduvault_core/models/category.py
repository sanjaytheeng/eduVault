from odoo import models, fields


class OpCategory(models.Model):
    _name = "op.category"
    _description = "eduvault Category"

    name = fields.Char('Name', size=256, required=True)
    code = fields.Char('Code', size=16, required=True)

    _sql_constraints = [
        ('unique_category_code',
         'unique(code)', 'Code should be unique per category!')]
