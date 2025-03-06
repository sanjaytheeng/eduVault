from odoo import api, fields, models

class Student(models.Model):
    _inherit = 'op.student'

    elearning_course_ids = fields.Many2many('slide.channel', string='eLearning Courses')
    elearning_tag_ids = fields.Many2many('slide.channel.tag', string='eLearning Tags')