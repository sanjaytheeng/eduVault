from odoo import api, models, fields, _
from datetime import timedelta

class OpAssignment(models.Model):
    _name="op.assignments"
    _description = "Assignments"
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _order = "id desc"

    name = fields.Char(string='Name', required=True)
    description = fields.Text(string='Description')
    start_date = fields.Datetime(string='Start Date',default= fields.Datetime.now, required=True)
    end_date = fields.Datetime(string='End Date', default=lambda self: fields.Datetime.now() + timedelta(days=2), required=True)
    course_id = fields.Many2one('op.course', string='Course', required=True)
    subject_id = fields.Many2one('op.subject', string='Subject', required=True)
    faculty_id = fields.Many2one('op.faculty', string='Faculty', required=True)
    assignment_lines = fields.One2many('op.assignment.line', 'assignment_id', string='Assignment Lines')
    state = fields.Selection([
        ('draft', 'Draft'),
        ('publish', 'Publish'),
        ('close', 'Close'),
        ('cancel', 'Cancel'),
    ], string='State', index=True, readonly=True, default='draft', track_visibility='onchange')
    total_assignment = fields.Integer(string='Total Assignment', compute='_compute_assignment')
    total_submitted = fields.Integer(string='Total Submitted', compute='_compute_assignment')
    total_not_submitted = fields.Integer(string='Total Not Submitted', compute='_compute_assignment')

    @api.depends('assignment_lines')
    def _compute_assignment(self):
        for record in self:
            record.total_assignment = len(record.assignment_lines)
            record.total_submitted = len(record.assignment_lines.filtered(lambda x: x.state == 'submit'))
            record.total_not_submitted = len(record.assignment_lines.filtered(lambda x: x.state == 'draft'))
    _description="List of all the assignments"

    name= fields.Char(string="Assignment Name", required=True)
    description= fields.Text(string="Description")
