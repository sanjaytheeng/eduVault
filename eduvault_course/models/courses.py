from odoo import models, fields

class InheritOpStudentCourse(models.Model):
    _inherit = "op.student.course"

    course_detail_id = fields.Many2one(
        'op.course', 'Course', required=True, readonly=True)
