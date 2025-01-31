from odoo import api, models, fields, _
from datetime import timedelta

class OpAssignment(models.Model):
    _name="op.assignments"
    _description = "Assignments"

    name = fields.Char(string='Assignment Name', required=True)
    description = fields.Text(string='Description')
    start_date = fields.Datetime(string='Assign Date',default= fields.Datetime.now, required=True)
    end_date = fields.Datetime(string='Submit By', default=lambda self: fields.Datetime.now() + timedelta(days=2), required=True)
    course_id = fields.Many2one('op.course', string='Course', required=True)
    batch_id = fields.Many2one('op.batch', string="Batch", help="Batch to assign thje assignment to")
    subject_id = fields.Many2one('op.subject', string='Subject', required=True)
    faculty_id = fields.Many2one('op.faculty', required=True, string="Teacher", help="Name of the teacher who gave this assignment")
    state = fields.Selection([
        ('draft', 'Draft'),
        ('publish', 'Publish'),
        ('close', 'Close'),
        ('cancel', 'Cancel'),
    ], string='State', index=True, readonly=True, default='draft', track_visibility='onchange')
    attachment = fields.Binary()
    total_assignment = fields.Integer(string='Total Assignment', compute='_compute_assignment')
    total_submitted = fields.Integer(string='Total Submitted', compute='_compute_assignment')
    total_not_submitted = fields.Integer(string='Total Not Submitted', compute='_compute_assignment')


    def _compute_submitted(self):
        for record in self:
            record.total_submitted =  len(record.assignment_line_ids.filtered(lambda l: l.state == 'submit'))

