import logging
from odoo import http
from odoo.http import request
import json

_logger = logging.getLogger(__name__)

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

            attendance_lines = request.env['op.attendance.line'].sudo().search(
                [('attendance_id', '=', attendance_sheet_id)])

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
                'attendance_date': attendance_sheet.attendance_date.strftime(
                    '%Y-%m-%d') if attendance_sheet.attendance_date else None,
                'attendance_records': attendance_data,
            }

            return request.make_response(json.dumps(response_data), headers={'Content-Type': 'application/json'})

        except Exception as e:
            _logger.error("Error fetching attendance sheet: %s", str(e))
            return request.make_response(json.dumps({'status': 'error', 'message': str(e)}),
                                         headers={'Content-Type': 'application/json'}, status=500)

class AttendanceController(http.Controller):

    @http.route('/api/attendance_sheets', type='http', auth='public', methods=['GET'], csrf=False)
    def get_all_attendance_sheets(self, **kwargs):
        """
        Fetch all attendance sheets.
        """
        try:
            attendance_sheets = request.env['op.attendance.sheet'].sudo().search([])

            if not attendance_sheets:
                return request.make_response(json.dumps({'error': 'No attendance sheets found'}),
                                             headers={'Content-Type': 'application/json'}, status=404)

            response_data = [{
                'attendance_sheet_id': sheet.id,
                'register_id' : sheet.register_id.name,
                'attendance_date': sheet.attendance_date.strftime('%Y-%m-%d') if sheet.attendance_date else None
            } for sheet in attendance_sheets]

            return request.make_response(json.dumps(response_data),
                                         headers={'Content-Type': 'application/json'})

        except Exception as e:
            _logger.error("Error fetching attendance sheets: %s", str(e))
            return request.make_response(json.dumps({'status': 'error', 'message': 'Internal server error'}),
                                         headers={'Content-Type': 'application/json'}, status=500)
