from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class OpFaculty(models.Model):
    _name = "op.faculty"
    _description = "eduvault Faculty"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _inherits = {"res.partner": "partner_id"}
    _parent_name = False

    partner_id = fields.Many2one('res.partner', 'Partner',
                                 required=True, ondelete="cascade")
    first_name = fields.Char('First Name', translate=True, required=True)
    middle_name = fields.Char('Middle Name', size=128)
    last_name = fields.Char('Last Name', size=128, required=True)
    birth_date = fields.Date('Birth Date', required=True)
    blood_group = fields.Selection([
        ('A+', 'A+ve'),
        ('B+', 'B+ve'),
        ('O+', 'O+ve'),
        ('AB+', 'AB+ve'),
        ('A-', 'A-ve'),
        ('B-', 'B-ve'),
        ('O-', 'O-ve'),
        ('AB-', 'AB-ve')
    ], string='Blood Group')
    gender = fields.Selection([
        ('male', 'Male'),
        ('female', 'Female')
    ], 'Gender', required=False)
    nationality = fields.Many2one('res.country', 'Nationality')
    emergency_contact = fields.Many2one(
        'res.partner', 'Emergency Contact')
    visa_info = fields.Char('Visa Info', size=64)
    id_number = fields.Char('ID Card Number', size=64)
    login = fields.Char(
        'Login', related='partner_id.user_id.login', readonly=True)
    last_login = fields.Datetime('Latest Connection', readonly=True,
                                 related='partner_id.user_id.login_date')
    faculty_subject_ids = fields.Many2many('op.subject', string='Subject(s)',
                                           tracking=True)
    emp_id = fields.Many2one('hr.employee', 'HR Employee')
    main_department_id = fields.Many2one(
        'op.department', 'Main Department',
        default=lambda self:
        self.env.user.dept_id and self.env.user.dept_id.id or False)
    allowed_department_ids = fields.Many2many(
        'op.department', string='Allowed Department',
        default=lambda self:
        self.env.user.department_ids and self.env.user.department_ids.ids or False)
    active = fields.Boolean(default=True)

    @api.constrains('birth_date')
    def _check_birthdate(self):
        for record in self:
            if record.birth_date > fields.Date.today():
                raise ValidationError(_(
                    "Birth Date can't be greater than current date!"))

    @api.onchange('first_name', 'middle_name', 'last_name')
    def _onchange_name(self):
        if not self.middle_name:
            self.name = str(self.first_name) + " " + str(
                self.last_name)
        else:
            self.name = str(self.first_name) + " " + str(
                self.middle_name) + " " + str(self.last_name)

    def create_employee(self):
        for record in self:
            vals = {
                'name': record.name,
                'country_id': record.nationality.id,
                'gender': record.gender,
                'private_state_id': record.partner_id.id
            }
            emp_id = self.env['hr.employee'].create(vals)
            record.write({'emp_id': emp_id.id})
            record.partner_id.write({'partner_share': True, 'employee': True})

    @api.model
    def get_import_templates(self):
        return [{
            'label': _('Import Template for Faculties'),
            'template': '/eduvault_core/static/xls/op_faculty.xls'
        }]

class HREmployee(models.Model):
    _inherit = "hr.employee"

    faculty_id = fields.Many2one('op.faculty', 'Faculty Record', readonly=True)

    faculty_id = fields.Many2one('op.faculty', 'Faculty Record', readonly=True)

    def action_create_faculty(self):
        """
        Button action to create or update a faculty record from an employee without requiring a user account.
        Uses fields from the custom op.faculty model.
        """
        for employee in self:
            # Initialize variables for first, middle, and last names
            first_name = ''
            middle_name = ''
            last_name = ''

            # Check if the employee has a name and split it into components
            if employee.name:
                name_parts = employee.name.split()
                first_name = name_parts[0] if len(name_parts) > 0 else ''
                middle_name = " ".join(name_parts[1:-1]) if len(name_parts) > 2 else ''
                last_name = name_parts[-1] if len(name_parts) > 1 else ''

            # Ensure partner_id is set or create a new partner if needed
            partner_vals = {
                'name': f"{first_name} {middle_name} {last_name}".strip(),
                # Use .strip() to remove any unnecessary spaces
            }

            # Create partner record if not already existing
            partner = employee.user_id.partner_id if employee.user_id else self.env['res.partner'].create(partner_vals)

            # Check if faculty record exists or create a new one
            if employee.faculty_id:
                # Update the existing faculty record
                faculty = employee.faculty_id
            else:
                # Create a new faculty record
                faculty_vals = {
                    'partner_id': partner.id,
                    'first_name': first_name,
                    'middle_name': middle_name,
                    'last_name': last_name,
                    'gender': employee.gender,
                    'email': employee.private_email,
                    'phone': employee.private_phone,
                    'birth_date': employee.birthday,
                    'emp_id': employee.id,
                }
                faculty = self.env['op.faculty'].create(faculty_vals)

            # Update faculty record with any new or changed data
            faculty.write({
                'first_name': first_name,
                'middle_name': middle_name,
                'last_name': last_name,
                'gender': employee.gender,
                'email': employee.private_email,
                'phone': employee.private_phone,
                'birth_date': employee.birthday,
            })

            # Link Faculty to Employee
            employee.faculty_id = faculty.id


