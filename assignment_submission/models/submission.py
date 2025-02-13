from odoo import models, fields, api

class StudentSubmission(models.Model):
    _name = "student.submission"
    _description = "Student Assignment Submission"

    student_id = fields.Many2one('res.partner', string="Student", required=True)
    assignment_id = fields.Many2one('op.assignments', string="Assignment", required=True)
    submission_date = fields.Datetime(string="Submission Date", default=fields.Datetime.now)
    file_attachment = fields.Binary(string="Attachment", required=True)
    state = fields.Selection([
        ('draft', 'Draft'),
        ('submit', 'Submitted'),
        ('graded', 'Graded'),
    ], string='State', default='draft')

    grade = fields.Float(string="Grade", help="Marks awarded for the assignment")

    @api.model
    def create(self, vals):
        """Override create method to automatically set submission state."""
        vals['state'] = 'submit'
        return super(StudentSubmission, self).create(vals)
