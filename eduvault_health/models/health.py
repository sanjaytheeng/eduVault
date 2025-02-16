from odoo import models, fields, api, _
from odoo.exceptions import ValidationError

class OpHealth(models.Model):
    _name = 'op.health'
    _rec_name = 'student_id'
    _description = """Health Detail for Students and Faculties"""

    type = fields.Selection(
        [('student', 'Student'), ('faculty', 'Faculty')],
        'Type', default='student', required=True)
    student_id = fields.Many2one('op.student', 'Student')
    faculty_id = fields.Many2one('op.faculty', 'Faculty')
    height = fields.Float('Height(C.M.)', required=True)
    weight = fields.Float('Weight', required=True)
    blood_group = fields.Selection(
        [('A+', 'A+ve'), ('B+', 'B+ve'), ('O+', 'O+ve'), ('AB+', 'AB+ve'),
         ('A-', 'A-ve'), ('B-', 'B-ve'), ('O-', 'O-ve'), ('AB-', 'AB-ve')],
        'Blood Group', required=True)
    physical_challenges = fields.Boolean('Physical Challenge?', default=False)
    physical_challenges_note = fields.Text('Physical Challenge')
    major_diseases = fields.Boolean('Major Diseases?', default=False)
    major_diseases_note = fields.Text('Major Diseases')
    eyeglasses = fields.Boolean('Eye Glasses?')
    eyeglasses_no = fields.Char('Eye Glasses', size=64)
    regular_checkup = fields.Boolean(
        'Any Regular Checkup Required?', default=False)
    health_line = fields.One2many(
        'op.health.line', 'health_id', 'Checkup Lines')

    @api.constrains('height', 'weight')
    def check_height_weight(self):
        if self.height <= 0.0 or self.weight <= 0.0:
            raise ValidationError(_("Enter proper height and weight!"))
