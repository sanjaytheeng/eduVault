from odoo import api, fields, models
import logging

_logger = logging.getLogger(__name__)

class ExtendCourse(models.Model):
    _inherit = 'op.course'  # Inherit from the 'op.course' model

    # Define the new fields
    elearning_tag_ids = fields.Many2many('slide.channel.tag', string='eLearning Tags')
    elearning_course_ids = fields.Many2many('slide.channel', string='eLearning Courses', compute="_compute_elearning_courses", store=True)

    @api.depends('elearning_tag_ids')
    def _compute_elearning_courses(self):
        for course in self:
            if course.elearning_tag_ids:
                # Search for all courses related to the selected tags
                related_courses = self.env['slide.channel'].search([
                    ('tag_ids', 'in', course.elearning_tag_ids.ids),
                    ('active', '=', True),  # Ensure the courses are active
                ])
                course.elearning_course_ids = related_courses
            else:
                course.elearning_course_ids = False