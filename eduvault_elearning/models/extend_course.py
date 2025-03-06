from odoo import api, fields, models
import logging

_logger = logging.getLogger(__name__)

class ExtendCourse(models.Model):
    _inherit = 'op.course'

    elearning_course_id = fields.Many2one('elearning.course', string='eLearning Course')
    elearning_tag_ids = fields.Many2many('elearning.tag', string='eLearning Tags')