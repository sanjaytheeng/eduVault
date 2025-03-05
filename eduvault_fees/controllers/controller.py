from odoo import http
from odoo.http import request
import json

class StudentFeesController(http.Controller):

    @http.route('/api/students/fees/details', type='http', auth='public', methods=['GET'], csrf=False)
    def get_all_students_fees_details(self, **kwargs):
        students = request.env['op.student'].sudo().search([])

        if not students:
            return request.make_response(json.dumps({'error': 'No students found'}),
                                         headers={'Content-Type': 'application/json'})

        all_fees_data = []
        for student in students:
            fees_details = student.fees_detail_ids
            fees_data = []
            for fee in fees_details:
                fees_data.append({
                    'fees_line_id': fee.fees_line_id.id if fee.fees_line_id else None,
                    'amount': fee.amount,
                    'date': fee.date.strftime('%Y-%m-%d') if fee.date else None,
                    'product_id': fee.product_id.id if fee.product_id else None,
                    'state': fee.state,
                    'discount': fee.discount,
                    'after_discount_amount': fee.after_discount_amount,
                    'invoice_state': fee.invoice_state,
                    'course_id': fee.course_id.id if fee.course_id else None,
                    'batch_id': fee.batch_id.id if fee.batch_id else None,
                })

            all_fees_data.append({
                'student_id': student.id,
                'student_name': student.name,
                'fees_details': fees_data,
            })

        return request.make_response(json.dumps({'status': 'success', 'data': all_fees_data}),
                                     headers={'Content-Type': 'application/json'})

class IndividualStudentFeesController(http.Controller):

    @http.route('/api/student/fees/details/<int:student_id>', type='http', auth='public', methods=['GET'], csrf=False)
    def get_student_fees_details(self, **kwargs):
        student_id = kwargs.get('student_id')

        if not student_id:
            return request.make_response(json.dumps({'error': 'Missing student_id'}),
                                         headers={'Content-Type': 'application/json'})

        student = request.env['op.student'].sudo().search([('id', '=', int(student_id))], limit=1)

        if not student:
            return request.make_response(json.dumps({'error': 'Student not found'}),
                                         headers={'Content-Type': 'application/json'})

        fees_details = student.fees_detail_ids

        fees_data = []
        for fee in fees_details:
            fees_data.append({
                'fees_line_id': fee.fees_line_id.id if fee.fees_line_id else None,
                'amount': fee.amount,
                'date': fee.date.strftime('%Y-%m-%d') if fee.date else None,
                'product_id': fee.product_id.id if fee.product_id else None,
                'state': fee.state,
                'discount': fee.discount,
                'after_discount_amount': fee.after_discount_amount,
                'invoice_state': fee.invoice_state,
                'course_id': fee.course_id.id if fee.course_id else None,
                'batch_id': fee.batch_id.id if fee.batch_id else None,
            })

        response_data = {
            'student_id': student.id,
            'student_name': student.name,
            'fees_details': fees_data,
        }

        return request.make_response(json.dumps(response_data), headers={'Content-Type': 'application/json'})


   