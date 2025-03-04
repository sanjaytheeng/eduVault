from odoo import http
from odoo.http import request
import json

class StudentAttendanceController(http.Controller):

    @http.route('/api/attendance_sheet/<int:attendance_sheet_id>', type='http', auth='public', methods=['GET'], csrf=False)
    def get_attendance_sheet(self, attendance_sheet_id, **kwargs):
        """
        Fetch the attendance records for a specific attendance sheet by ID.
        """
        try:
            attendance_sheet = request.env['op.attendance.sheet'].sudo().browse(attendance_sheet_id)

            if not attendance_sheet.exists():
                return request.make_response(json.dumps({'error': 'Attendance sheet not found'}),
                                             headers={'Content-Type': 'application/json'}, status=404)

            attendance_lines = request.env['op.attendance.line'].sudo().search([('attendance_id', '=', attendance_sheet_id)])

            attendance_data = [{
                'student_id': line.student_id.id,
                'student_name': line.student_id.name,
                'attendance_date': line.attendance_date.strftime('%Y-%m-%d') if line.attendance_date else None,
                'present': line.present,
                'absent': line.absent,
                'remark': line.remark or None,
            } for line in attendance_lines]

            response_data = {
                'attendance_sheet_id': attendance_sheet.id,
                'attendance_date': attendance_sheet.attendance_date.strftime('%Y-%m-%d') if attendance_sheet.attendance_date else None,
                'attendance_records': attendance_data,
            }

            return request.make_response(json.dumps(response_data), headers={'Content-Type': 'application/json'})

        except Exception as e:
            _logger.error("Error fetching attendance sheet: %s", str(e))
            return request.make_response(json.dumps({'status': 'error', 'message': str(e)}),
                                         headers={'Content-Type': 'application/json'}, status=500)