import logging
from odoo import http
from odoo.http import request, Response
import json

_logger = logging.getLogger(__name__)

class MarksheetController(http.Controller):

    @http.route('/api/marksheet_lines', type='http', auth='public', methods=['GET'], csrf=False)
    def get_all_marksheet_lines(self, **kwargs):
        try:
            # Fetch all marksheet lines
            marksheet_lines = request.env['op.marksheet.line'].sudo().search([])

            # Format marksheet data
            marksheet_data = []
            for line in marksheet_lines:
                student = line.student_id
                marksheet_data.append({
                    'student_name': student.name,
                    'grade': line.grade,  # Using the computed grade directly
                    'status': line.status,  # Using the computed status directly
                    'percentage': line.percentage,  # Using the computed percentage directly
                })

            return Response(json.dumps({'status': 'success', 'data': marksheet_data}),
                            content_type='application/json', status=200)

        except Exception as e:
            _logger.error("Error fetching marksheet lines: %s", str(e))
            return Response(json.dumps({'status': 'error', 'message': str(e)}),
                            content_type='application/json', status=500)

class IndividualMarksheetController(http.Controller):

    @http.route('/api/marksheet_lines/<int:student_id>', type='http', auth='public', methods=['GET'], csrf=False)
    def get_marksheet_for_student(self, student_id, **kwargs):
        try:
            # Fetch marksheet lines for a specific student
            marksheet_lines = request.env['op.marksheet.line'].sudo().search([('student_id', '=', student_id)])

            # If no marksheet lines found for the student
            if not marksheet_lines:
                return Response(json.dumps({'status': 'error', 'message': 'No marksheet found for this student'}),
                                content_type='application/json', status=404)

            # Format marksheet data
            marksheet_data = []
            for line in marksheet_lines:
                student = line.student_id
                marksheet_data.append({
                    'student_name': student.name,
                    'grade': line.grade,  # Using the computed grade directly
                    'status': line.status,  # Using the computed status directly
                    'percentage': line.percentage,  # Using the computed percentage directly
                })

            return Response(json.dumps({'status': 'success', 'data': marksheet_data}),
                            content_type='application/json', status=200)

        except Exception as e:
            _logger.error("Error fetching marksheet lines for student %d: %s", student_id, str(e))
            return Response(json.dumps({'status': 'error', 'message': str(e)}),
                            content_type='application/json', status=500)
