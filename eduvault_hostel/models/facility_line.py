from odoo import models, fields

class OpFacilityLine(models.Model):
    _inherit = 'op.facility.line'

    room_id = fields.Many2one('op.room', string='Room')
