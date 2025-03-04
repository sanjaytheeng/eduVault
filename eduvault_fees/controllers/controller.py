from odoo import http
from odoo.http import request
import json


class StudentFeesController(http.Controller):

    @http.route('/api/student/fees/details', type='http', auth='public', methods=['GET'], csrf=False)
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


    @http.route('/api/student/fees/invoice/create', type='http', auth='public', methods=['POST'], csrf=False)
    def create_student_invoice(self, **kwargs):
        student_id = kwargs.get('student_id')
        product_id = kwargs.get('product_id')
        amount = kwargs.get('amount')
        discount = kwargs.get('discount', 0.0)

        if not student_id or not product_id or not amount:
            return request.make_response(json.dumps({'error': 'Missing required parameters'}),
                                         headers={'Content-Type': 'application/json'})

        student = request.env['op.student'].sudo().search([('id', '=', int(student_id))], limit=1)

        if not student:
            return request.make_response(json.dumps({'error': 'Student not found'}),
                                         headers={'Content-Type': 'application/json'})

        product = request.env['product.product'].sudo().search([('id', '=', int(product_id))], limit=1)

        if not product:
            return request.make_response(json.dumps({'error': 'Product not found'}),
                                         headers={'Content-Type': 'application/json'})

        # Create the fees details record first
        fees_detail = request.env['op.student.fees.details'].sudo().create({
            'student_id': student.id,
            'product_id': product.id,
            'amount': float(amount),
            'discount': float(discount),
            'state': 'draft',  # Initial state
        })

        # Create the invoice from the fees details
        fees_detail.get_invoice()

        response_data = {
            'invoice_id': fees_detail.invoice_id.id,
            'student_id': student.id,
            'amount': fees_detail.amount,
            'discount': fees_detail.discount,
            'after_discount_amount': fees_detail.after_discount_amount,
            'state': fees_detail.state,
        }

        return request.make_response(json.dumps(response_data), headers={'Content-Type': 'application/json'})


    @http.route('/api/student/fees/view_invoice', type='http', auth='public', methods=['GET'], csrf=False)
    def view_student_invoice(self, **kwargs):
        student_id = kwargs.get('student_id')

        if not student_id:
            return request.make_response(json.dumps({'error': 'Missing student_id'}),
                                         headers={'Content-Type': 'application/json'})

        student = request.env['op.student'].sudo().search([('id', '=', int(student_id))], limit=1)

        if not student:
            return request.make_response(json.dumps({'error': 'Student not found'}),
                                         headers={'Content-Type': 'application/json'})

        # Fetch existing invoices
        if student.invoice_id:
            invoice = student.invoice_id
            invoice_data = {
                'invoice_id': invoice.id,
                'partner_id': invoice.partner_id.id,
                'amount_total': invoice.amount_total,
                'state': invoice.state,
                'invoice_date': invoice.invoice_date.strftime('%Y-%m-%d') if invoice.invoice_date else None,
                'invoice_line_ids': [{
                    'product_id': line.product_id.id,
                    'product_name': line.product_id.name,
                    'quantity': line.quantity,
                    'price_unit': line.price_unit,
                    'discount': line.discount,
                } for line in invoice.invoice_line_ids]
            }
            return request.make_response(json.dumps(invoice_data), headers={'Content-Type': 'application/json'})
        else:
            return request.make_response(json.dumps({'message': 'No invoice found for this student.'}),
                                         headers={'Content-Type': 'application/json'})
