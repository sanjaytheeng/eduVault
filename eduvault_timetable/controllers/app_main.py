from odoo import http
from odoo.http import request
import json


class StudentAttendanceController(http.Controller):

    @http.route('/api/student_attendance', type='http', auth='public', methods=['GET'], csrf=False)
    def get_student_attendance(self, **kwargs):
        student_id = kwargs.get('student_id')

        if not student_id:
            return request.make_response(json.dumps({'error': 'Missing student_id'}),
                                         headers={'Content-Type': 'application/json'})

        student = request.env['op.student'].sudo().search([('id', '=', int(student_id))], limit=1)

        if not student:
            return request.make_response(json.dumps({'error': 'Student not found'}),
                                         headers={'Content-Type': 'application/json'})

        attendance_records = request.env['op.attendance.line'].sudo().search([('student_id', '=', student.id)])

        attendance_data = []
        for record in attendance_records:
            attendance_data.append({
                'attendance_id': record.attendance_id.id,
                'attendance_date': record.attendance_date.strftime('%Y-%m-%d') if record.attendance_date else None,
                'present': record.present,
                'excused': record.excused,
                'absent': record.absent,
                'late': record.late,
                'course': record.course_id.name if record.course_id else None,
                'batch': record.batch_id.name if record.batch_id else None,
                'remark': record.remark or None,
            })

        response_data = {
            'student_id': student.id,
            'student_name': student.name,
            'attendance_records': attendance_data,
        }

        return request.make_response(json.dumps(response_data), headers={'Content-Type': 'application/json'})