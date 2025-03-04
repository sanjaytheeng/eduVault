from odoo import models, fields

class InheritOpStudentCourse(models.Model):
    _inherit = "op.student.course"

    course_detail_ids = fields.One2many('op.student.course', 'student_id', string="Student Courses")
