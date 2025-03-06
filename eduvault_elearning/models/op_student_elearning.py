from odoo import models, fields

class OpStudentElearning(models.Model):
    _inherit = "op.student"

    course_ids = fields.Many2many('slide.channel', string="Enrolled eLearning Courses")
    course_progress = fields.One2many('slide.slide.partner', 'partner_id', string="Course Progress")
