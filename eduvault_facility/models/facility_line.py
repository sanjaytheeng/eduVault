

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class OpFacilityLine(models.Model):
    _name = "op.facility.line"
    _rec_name = "facility_id"
    _description = "Manage Facility Line"

    facility_id = fields.Many2one('op.facility', 'Facility', required=True)
    quantity = fields.Float('Quantity', required=True)

    @api.constrains('quantity')
    def check_quantity(self):
        for record in self:
            if record.quantity <= 0.0:
                raise ValidationError(_("Enter proper Quantity in Facilities!"))
