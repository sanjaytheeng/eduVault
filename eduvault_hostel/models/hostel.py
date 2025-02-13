from odoo import models, fields, api, _
from odoo.exceptions import ValidationError

class OpHostel(models.Model):
    _name = 'op.hostel'
    _description = 'Hostel'

    name = fields.Char(string='Name', size=16, required=True)
    capacity = fields.Integer(string='Hostel Capacity', required=True)
    hostel_room_lines = fields.One2many('op.hostel.room', 'hostel_id', string='Room(s)')
    students_per_room = fields.Integer(string="Students per Room", required=False)
    students_count = fields.Integer(string="Student Count", compute="_compute_students_count", store=True)
    booking_schedule = fields.Datetime(string="Booking Schedule")

    @api.depends('hostel_room_lines.students_per_room')
    def _compute_students_count(self):
        for record in self:
            record.students_count = sum(room.students_per_room for room in record.hostel_room_lines)

    @api.constrains('hostel_room_lines', 'capacity')
    def _check_hostel_capacity(self):
        for record in self:
            if record.capacity <= 0:
                raise ValidationError(_('Enter a proper Hostel Capacity'))

            total_students = sum(room.students_per_room for room in record.hostel_room_lines)

            if total_students > record.capacity:
                raise ValidationError(_('Hostel Capacity Over'))
