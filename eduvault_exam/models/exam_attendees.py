
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class OpExamAttendees(models.Model):
    _name = "op.exam.attendees"
    _rec_name = "student_id"
    _description = "Exam Attendees"

    student_id = fields.Many2one('op.student', 'Student', required=True)
    status = fields.Selection(
        [('present', 'Present'), ('absent', 'Absent')],
        'Status', default="present", required=True)
    marks = fields.Integer('Marks')
    note = fields.Text('Note')
    exam_id = fields.Many2one(
        'op.exam', 'Exam', required=True, ondelete="cascade")
    course_id = fields.Many2one('op.course', 'Course', readonly=True)
    batch_id = fields.Many2one('op.batch', 'Batch', readonly=True)
    room_id = fields.Many2one('op.exam.room', 'Room')

    _sql_constraints = [
        ('unique_attendees',
         'unique(student_id,exam_id)',
         'Attendee must be unique per exam.'),
    ]

    @api.onchange('exam_id')
    def onchange_exam(self):
        self.course_id = self.exam_id.session_id.course_id
        self.batch_id = self.exam_id.session_id.batch_id
        self.student_id = False

    @api.constrains('marks')
    def _check_marks(self):
        if self.marks < 0.0 or self.marks > self.exam_id.total_marks:
            raise ValidationError(_("Please Enter Marks between 0 to %d" %self.exam_id.total_marks))
