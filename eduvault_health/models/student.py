from odoo import models, fields

class OpStudent(models.Model):

    _inherit = 'op.student'

    health_lines = fields.One2many('op.health', 'student_id', 'Health Detail')
