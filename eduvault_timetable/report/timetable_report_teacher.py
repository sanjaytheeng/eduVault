
import calendar
import pytz
import time
from datetime import datetime
from odoo import models, api, _, tools, fields


class ReportTimeTableTeacherGenerate(models.AbstractModel):
    _name = "report.eduvault_timetable.report_timetable_teacher_generate"
    _description = "Timetable Teacher Report"

    def _convert_to_local_timezone(self, time):
        '''
            Converts time as per local timezone.
        '''
        if time:
            timezone = pytz.timezone(self._context['tz'] or 'UTC')
            utc_in_time = pytz.UTC.localize(fields.Datetime.from_string(time))
            local_time = utc_in_time.astimezone(timezone)
            return local_time

    def get_full_name(self, data):
        faculty_name = self.env['op.faculty'].browse(data['faculty_id'][0])
        return faculty_name.name

    def sort_tt(self, data_list):
        main_list = []
        f = []
        for d in data_list:
            if d['period'] not in f:
                f.append(d['period'])
                main_list.append({
                    'name': d['period'],
                    'line': {d['day']: d},
                    'peropd_time': ' To '.join([d['start_datetime'],
                                                d['end_datetime']])
                })
            else:
                for m in main_list:
                    if m['name'] == d['period']:
                        m['line'][d['day']] = d
        return main_list

    def get_heading(self):
        dayofWeek = [_(calendar.day_name[0]),
                     _(calendar.day_name[1]),
                     _(calendar.day_name[2]),
                     _(calendar.day_name[3]),
                     _(calendar.day_name[4]),
                     _(calendar.day_name[5]),
                     _(calendar.day_name[6])]
        return dayofWeek

    def get_object(self, data):
        data_list = []
        for timetable_obj in self.env['op.session'].browse(
                data['teacher_time_table_ids']):
            oldDate = pytz.UTC.localize(
                fields.Datetime.from_string(timetable_obj.start_datetime))
            day = datetime.weekday(oldDate)
            timetable_data = {
                'period': timetable_obj.timing,
                # 'period_time': timetable_obj.timing_id.hour + ':' +
                # timetable_obj.timing_id.minute +
                # timetable_obj.timing_id.am_pm,
                'start_datetime': self._convert_to_local_timezone(
                    timetable_obj.start_datetime).strftime(
                    tools.DEFAULT_SERVER_DATETIME_FORMAT),
                'end_datetime': self._convert_to_local_timezone(
                    timetable_obj.end_datetime).strftime(
                    tools.DEFAULT_SERVER_DATETIME_FORMAT),
                'day': str(day),
                'subject': timetable_obj.subject_id.name,
                'course': timetable_obj.course_id.name,
                'batch': timetable_obj.batch_id.name,
            }
            data_list.append(timetable_data)
        ttdl = sorted(data_list, key=lambda k: k['start_datetime'])
        final_list = self.sort_tt(ttdl)
        return final_list

    @api.model
    def _get_report_values(self, docids, data=None):
        model = self.env.context.get('active_model')
        docs = self.env[model].browse(self.env.context.get('active_id'))
        docargs = {
            'doc_ids': self.ids,
            'doc_model': model,
            'docs': docs,
            'data': data,
            'time': time,
            'get_object': self.get_object,
            'get_heading': self.get_heading,
            'get_full_name': self.get_full_name,
        }
        return docargs
