from odoo import models, fields, api
from odoo.exceptions import UserError


class Alumni(models.Model):
    _name = 'alumni.alumni'
    _description = 'Alumni Record'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    first_name = fields.Char('First Name', translate=True)
    middle_name = fields.Char('Middle Name', translate=True)
    last_name = fields.Char('Last Name', translate=True)
    email = fields.Char(string='Email')
    mobile = fields.Char(string='Mobile')
    address = fields.Text(string='Address')

    student_id = fields.Many2one('op.student', string='Student Reference')
    course_id = fields.Many2one('op.course', 'Course')
    batch_id = fields.Many2one('op.batch', 'Batch')
    graduation_year = fields.Integer(string='Graduation Year')

    company = fields.Char(string='Company')
    position = fields.Char(string='Position')
    industry = fields.Char(string='Industry')
    experience = fields.Integer(string='Years of Experience')

    mentorship = fields.Boolean(string='Willing to Mentor')
    event_participation = fields.Boolean(string='Interested in Events')
    donation_contributor = fields.Boolean(string='Willing to Donate')

    graduation_date = fields.Date(string='Graduation Date', store=True)

    def create_from_student(self, student):
        """ Convert student record into an alumni record when they graduate. """
        if not student:
            raise UserError("Student record is missing!")

        alumni_vals = {
            'first_name': student.first_name,
            'middle_name': student.middle_name,
            'last_name': student.last_name,
            'email': student.email,
            'mobile': student.mobile,
            'address': student.street,
            'student_id': student.id,
        }
        return self.create(alumni_vals)


class OpStudentInherit(models.Model):
    _inherit = 'op.student'

    alumni_id = fields.Many2one('alumni.alumni', string='Alumni Record')
    is_alumni = fields.Boolean(string='Is Alumni', default=False)

    def create_alumni_from_student(self):
        """ Convert the student to alumni when the button is clicked. """
        self.write({'is_alumni': True})
        for student in self:
            if student.alumni_id:
                raise UserError("This student is already an alumni!")

            # Call the alumni model's create_from_student method
            alumni = self.env['alumni.alumni'].create_from_student(student)
            student.alumni_id = alumni.id  # Link the newly created alumni record

        return True  # Return True to avoid Odoo errors

    def is_alumni_installed(self):
        """ Check if the alumni module is installed. """
        alumni_module = self.env['ir.module.module'].search([('name', '=', 'eduvault_alumni')], limit=1)
        return alumni_module.state == 'installed'
