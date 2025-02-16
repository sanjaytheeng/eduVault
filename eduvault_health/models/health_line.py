

from odoo import models, fields


class OpHealthLine(models.Model):
    _name = 'op.health.line'

    health_id = fields.Many2one('op.health', 'Health')
    date = fields.Date('Date', default=lambda self: fields.Date.today())
    name = fields.Text('Checkup Detail', required=True)
    recommendation = fields.Text('Checkup Recommendation')
