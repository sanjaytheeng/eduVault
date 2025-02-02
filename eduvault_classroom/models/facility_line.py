

from odoo import models, fields


class OpFacilityLine(models.Model):
    _inherit = "op.facility.line"

    classroom_id = fields.Many2one('op.classroom', 'Classroom')

    _sql_constraints = [
        ('unique_facility_classroom',
         'UNIQUE(facility_id, classroom_id)',
         'Facility name exists. Please choose a unique name or update the quantity.')]
