from odoo import http
from odoo.http import request

class StudentFeesController(http.Controller):

    @http.route('/api/student_fees', type='json', auth='public', methods=['POST'], csrf=False)
    def get_student_fees(self, **kwargs):
        """
        Get the total fees amount for a given student.
        Request body should contain 'student_id'.
        """
        student_id = kwargs.get('student_id')

        if not student_id:
            return {'error': 'Missing student_id'}

        student = request.env['op.student'].sudo().search([('id', '=', student_id)], limit=1)

        if not student:
            return {'error': 'Student not found'}

        # Calculate the total fees
        total_fees = sum(student.fees_detail_ids.mapped('amount'))

        return {
            'student_id': student.id,
            'student_name': student.name,
            'total_fees': total_fees,
        }
