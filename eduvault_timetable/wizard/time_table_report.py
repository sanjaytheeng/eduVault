

from datetime import datetime
from datetime import timedelta

from dateutil.relativedelta import relativedelta
from odoo.exceptions import ValidationError

from odoo import models, fields, api, _


class SessionReport(models.TransientModel):
    _name = "time.table.report"
    _description = "Generate Time Table Report"

    state = fields.Selection(
        [('faculty', 'Faculty'), ('student', 'Student')],
        string='Select', required=True, default='faculty')
    course_id = fields.Many2one('op.course', 'Course')
    batch_id = fields.Many2one('op.batch', 'Batch')
    faculty_id = fields.Many2one('op.faculty', 'Faculty')
    start_date = fields.Date(
        'Start Date', required=True,
        default=(datetime.today() - relativedelta(
            days=datetime.date(
                datetime.today()).weekday())).strftime('%Y-%m-%d'))
    end_date = fields.Date(
        'End Date', required=True,
        default=(datetime.today() + relativedelta(days=6 - datetime.date(
            datetime.today()).weekday())).strftime('%Y-%m-%d'))

    @api.constrains('start_date', 'end_date')
    def _check_dates(self):
        for session in self:
            start_date = fields.Date.from_string(session.start_date)
            end_date = fields.Date.from_string(session.end_date)
            if end_date < start_date:
                raise ValidationError(_('End Date cannot be set before \
                Start Date.'))
            elif end_date > (start_date + timedelta(days=6)):
                raise ValidationError(_("Select date range for a week!"))

    @api.onchange('course_id')
    def onchange_course(self):
        if self.batch_id and self.course_id:
            if self.batch_id.course_id != self.course_id:
                self.batch_id = False

    def gen_time_table_report(self):
        template = self.env.ref(
            'eduvault_timetable.report_teacher_timetable_generate')
        data = self.read(
            ['start_date', 'end_date', 'course_id', 'batch_id', 'state',
             'faculty_id'])[0]
        if data['state'] == 'student':
            time_table_ids = self.env['op.session'].search(
                [('course_id', '=', data['course_id'][0]),
                 ('batch_id', '=', data['batch_id'][0]),
                 ('start_datetime', '>=', data['start_date']),
                 ('end_datetime', '<=', data['end_date'])],
                order='start_datetime asc')
            data.update({'time_table_ids': time_table_ids.ids})
            template = self.env.ref(
                'eduvault_timetable.report_student_timetable_generate')
        else:
            teacher_time_table_ids = self.env['op.session'].search(
                [('start_datetime', '>=', data['start_date']),
                 ('end_datetime', '<=', data['end_date']),
                 ('faculty_id', '=', data['faculty_id'][0])],
                order='start_datetime asc')
            data.update({'teacher_time_table_ids': teacher_time_table_ids.ids})
        return template.report_action(self, data=data)
