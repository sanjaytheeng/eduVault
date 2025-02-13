

from odoo import models, fields


class OpStudent(models.Model):
    _inherit = "op.student"

    allocation_ids = fields.Many2many('op.assignment', string='Assignment(s)')
    assignment_count = fields.Integer(compute='compute_count_assignment')

    def get_assignment(self):
        action = self.env.ref('eduvault_assignment.'
                              'act_open_op_assignment_view').read()[0]
        action['domain'] = [('allocation_ids', 'in', self.ids)]
        return action

    def compute_count_assignment(self):
        for record in self:
            record.assignment_count = self.env['op.assignment'].search_count(
                [('allocation_ids', '=', self.id)])
