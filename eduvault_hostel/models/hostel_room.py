from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class OpHostelRoomAllocation(models.Model):
    _name = 'op.hostel.room'
    _description = 'Hostel Room Allocation'

    hostel_id = fields.Many2one('op.hostel', string='Hostel', required=True)
    name = fields.Many2one('op.room', string='Room', required=True)
    room_capacity = fields.Integer(string="Room Capacity", required=True)
    student_ids = fields.Many2many('res.partner', string='Allocated Students')
    students_per_room = fields.Integer(string='Students per Room', required=True)
    rent = fields.Float(string='Rent')
    allocated_date = fields.Date(string='Allocated Date', default=fields.Date.context_today)

    @api.constrains('students_per_room')
    def _check_capacity(self):
        for record in self:
            if record.students_per_room <= 0:
                raise ValidationError(_('Enter a valid number for Students per Room'))

    @api.onchange('hostel_id')
    def _onchange_hostel(self):
        self.name = False

    @api.onchange('name')
    def _onchange_name(self):
        if self.name:
            self.students_per_room = self.name.capacity

    @api.constrains('student_ids', 'students_per_room')
    def _check_student_capacity(self):
        for record in self:
            if len(record.student_ids) > record.students_per_room:
                raise ValidationError(_('Room capacity exceeded'))