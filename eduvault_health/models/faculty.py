

from odoo import models, fields


class OpFaculty(models.Model):

    _inherit = 'op.faculty'

    health_faculty_lines = fields.One2many(
        'op.health', 'faculty_id', 'Health Detail')
