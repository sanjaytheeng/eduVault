from odoo import fields, api, models, _

class OpAssignmentLines(models.Model):
    _name="op.assignment.lines"
    _description="These right here are some assignment lines"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'id desc'
    
    name = fields.Char(string='Name', required=True)
    description = fields.Text(string='Description')
    assignment_id = fields.Many2one('op.assignments', string='Assignment')
    student_id = fields.Many2one('op.student', string='Student')
    submission_date = fields.Datetime(string='Submission Date', default=fields.Datetime.now)
    state = fields.Selection([
        ('draft', 'Draft'),
        ('submit', 'Submit'),
        ('late', 'Late'),
        ('done', 'Done'),
    ], string='State', index=True, readonly=True, default='draft', track_visibility='onchange')
    faculty_remark = fields.Text(string='Faculty Remark')
    
    def action_submit(self):
        for record in self:
            record.state = 'submit'
    
    def action_done(self):
        for record in self:
            record.state = 'done'
    
    def action_draft(self):
        for record in self:
            record.state = 'draft'
    
    def action_late(self):
        for record in self:
            record.state = 'late'