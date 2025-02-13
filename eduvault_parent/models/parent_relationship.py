

from odoo import models, fields


class OpParentRelation(models.Model):
    _name = "op.parent.relationship"
    _description = "Relationships"

    name = fields.Char('Name', required=True)

    _sql_constraints = [(
        'unique_relationship_name',
        'unique(name)',
        'Can not create relationship multiple times.!'
    )]