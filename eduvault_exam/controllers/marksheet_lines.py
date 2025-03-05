import logging
from odoo import http
from odoo.http import request, Response
import json

_logger = logging.getLogger(__name__)

class MarksheetController(http.Controller):

    @http.route('/api/marksheet/student/<int:student_id>', type='http', auth='public', methods=['GET'], csrf=False)
    def get_student_marksheet(self, student_id, **kwargs):
        try:
            # Fetch the student
            student = request.env['op.student'].sudo().browse(student_id)

            if not student.exists():
                return Response(json.dumps({'error': 'Student not found'}), content_type='application/json', status=404)

            # Fetch the marksheet lines related to the student
            marksheet_lines = request.env['op.marksheet.line'].sudo().search([('marksheet_reg_id.student_id', '=', student_id)])

            # Format marksheet data
            marksheet_data = []
            for line in marksheet_lines:
                subject = line.subject_id
                total_marks = line.marks
                percentage = (total_marks / line.marksheet_reg_id.total_marks) * 100 if line.marksheet_reg_id.total_marks else 0
                status = 'Pass' if percentage >= 40 else 'Fail'  # Assuming 40% is the passing mark
                grade = line.grade

                marksheet_data.append({
                    'student_name': student.name,
                    'subject': subject.name,
                    'total_marks': total_marks,
                    'status': status,
                    'percentage': percentage,
                    'grade': grade,
                })

            return Response(json.dumps({'status': 'success', 'data': marksheet_data}),
                            content_type='application/json', status=200)

        except Exception as e:
            _logger.error("Error fetching marksheet: %s", str(e))
            return Response(json.dumps({'status': 'error', 'message': str(e)}),
                            content_type='application/json', status=500)