from odoo import api, fields, models

class Student(models.Model):
    _inherit = 'op.student'

    # student_elearning_tag_ids = fields.Many2many(related='course_id.elearning_tag_ids', string='eLearning Tags', store=True)
    # student_elearning_course_ids = fields.Many2many(related='course_id.elearning_course_ids', string='eLearning Courses', store=True)

# from odoo import api, fields, models
#
# class Student(models.Model):
#     _inherit = 'op.student'
#
#     elearning_course_ids = fields.Many2many('slide.channel', string='eLearning Courses', compute="_compute_elearning_courses", store=True)
#     elearning_tag_ids = fields.Many2many('slide.channel.tag', string='eLearning Tags')
#
#     @api.depends('elearning_tag_ids')
#     def _compute_elearning_courses(self):
#         for course in self:
#             if course.elearning_tag_ids:
#                 # Search for all courses related to the selected tags
#                 related_courses = self.env['slide.channel'].search([
#                     ('tag_ids', 'in', course.elearning_tag_ids.ids),
#                     ('active', '=', True),  # Ensure the courses are active
#                 ])
#                 course.elearning_course_ids = related_courses
#             else:
#                 course.elearning_course_ids = False