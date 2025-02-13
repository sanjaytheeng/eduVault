from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class OpRoom(models.Model):
    _name = 'op.room'
    _description = 'Hostel Room'

    hostel_id = fields.Many2one('op.hostel', string='Hostel', required=True)
    name = fields.Char(string='Room Name', required=True)
    code = fields.Char(string='Code', required=True)
    capacity = fields.Integer(string='Room Capacity', required=True)
    start_date = fields.Datetime('Start Date')
    end_date = fields.Datetime('End Date')
    remaining_capacity = fields.Integer(
        string='Remaining Capacity',
        compute='_compute_remaining_capacity',
        store=True
    )
    facility_line = fields.One2many('op.facility.line', 'room_id', string='Facility')

    # Define the computed field for facilities count
    facilities_count = fields.Integer(
        string='Number of Facilities',
        compute='_compute_facilities_count',
        store=True
    )

    # Define the One2many field linking students to rooms
    student_ids = fields.One2many('op.student', 'room_id',
                                  string='Students')  # Assuming you have a model 'op.student' with a 'room_id' field

    # Define a computed field for students count
    students_count = fields.Integer(
        string='Number of Students',
        compute='_compute_students_count',
        store=True
    )

    @api.depends('capacity', 'students_count')
    def _compute_remaining_capacity(self):
        for room in self:
            room.remaining_capacity = room.capacity - room.students_count

    @api.depends('student_ids')
    def _compute_students_count(self):
        for room in self:
            room.students_count = len(room.student_ids)

    @api.depends('facility_line')
    def _compute_facilities_count(self):
        for room in self:
            room.facilities_count = len(room.facility_line)

    @api.constrains('capacity')
    def _check_capacity(self):
        for record in self:
            if record.capacity <= 0:
                raise ValidationError(_('Enter a valid Room Capacity'))
