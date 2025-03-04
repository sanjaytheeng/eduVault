import json
import logging
import base64
from odoo import http
from odoo.http import request, Response

_logger = logging.getLogger(__name__)

class StudentController(http.Controller):

    # GET all students
    @http.route('/api/students', type='http', auth='public', methods=['GET'], cors='*', csrf=False)
    def get_students(self):
        students = request.env['op.student'].sudo().search([])
        student_list = []

        for student in students:
            student_list.append({
                'id': student.id,
                'name': student.name,
                'first_name': student.first_name,
                'middle_name': student.middle_name or None,
                'last_name': student.last_name,
                'gender': student.gender,
                'birth_date': str(student.birth_date) if student.birth_date else None,
                'email': student.partner_id.email or None,
                'phone': student.partner_id.mobile or None,
                'gr_no': student.gr_no or None,
                'category': student.category_id.name if student.category_id else None,
                'image_url': f"/api/students/image/{student.id}" if student.partner_id.image_1920 else None,
            })

        return Response(json.dumps(student_list), content_type='application/json')

    # GET a single student by ID
    @http.route('/api/students/<int:student_id>', type='http', auth='public', methods=['GET'])
    def get_student(self, student_id):
        student = request.env['op.student'].sudo().browse(student_id)

        if not student.exists():
            return Response(json.dumps({'error': 'Student not found'}), content_type='application/json', status=404)

        student_data = {
            'id': student.id,
            'name': student.name,
            'first_name': student.first_name,
            'middle_name': student.middle_name or None,
            'last_name': student.last_name,
            'gender': student.gender,
            'birth_date': str(student.birth_date) if student.birth_date else None,
            'email': student.partner_id.email or None,
            'phone': student.partner_id.mobile or None,
            'gr_no': student.gr_no or None,
            'category': student.category_id.name if student.category_id else None,
            'image_url': f"/api/students/image/{student.id}" if student.partner_id.image_1920 else None,
        }

        return Response(json.dumps(student_data), content_type='application/json')

    # GET Student Image
    @http.route('/api/students/image/<int:student_id>', type='http', auth='public', methods=['GET'], cors='*', csrf=False)
    def get_student_image(self, student_id):
        student = request.env['op.student'].sudo().browse(student_id)

        if not student.exists() or not student.partner_id.image_1920:
            return Response(json.dumps({'error': 'Image not found'}), content_type='application/json', status=404)

        image_data = base64.b64decode(student.partner_id.image_1920)
        return request.make_response(image_data, headers=[('Content-Type', 'image/png')])

    # POST - Create a new student
    @http.route('/api/students', type='http', auth='public', methods=['POST'], csrf=False)
    def create_student(self, **kwargs):
        try:
            data = json.loads(request.httprequest.data)
            _logger.info("Received Data: %s", data)

            if not data.get('first_name') or not data.get('last_name'):
                return Response(json.dumps({'error': 'Fields "first_name" and "last_name" are required.'}), content_type='application/json')

            new_partner = request.env['res.partner'].sudo().create({
                'name': f"{data.get('first_name')} {data.get('last_name')}",
                'email': data.get('email', ''),
                'phone': data.get('phone', ''),
                'image_1920': data.get('image') if data.get('image') else None,  # Base64 Image
            })

            new_student = request.env['op.student'].sudo().create({
                'first_name': data.get('first_name'),
                'middle_name': data.get('middle_name', ''),
                'last_name': data.get('last_name'),
                'gender': data.get('gender', ''),
                'birth_date': data.get('birth_date', ''),
                'gr_no': data.get('gr_no', ''),
                'category_id': data.get('category_id'),
                'partner_id': new_partner.id,
            })

            return Response(json.dumps({'id': new_student.id, 'status': 'Student created successfully'}), content_type='application/json')
        except Exception as e:
            _logger.error("Error processing request: %s", str(e))
            return Response(json.dumps({'error': 'Invalid JSON format'}), content_type='application/json')

    # PUT - Update an existing student
    @http.route('/api/students/<int:student_id>', type='http', auth='public', methods=['PUT'], csrf=False)
    def update_student(self, student_id, **kwargs):
        data = json.loads(request.httprequest.data)
        student = request.env['op.student'].sudo().browse(student_id)

        if not student.exists():
            return Response(json.dumps({'error': 'Student not found'}), content_type='application/json', status=404)

        student.write({
            'first_name': data.get('first_name', student.first_name),
            'middle_name': data.get('middle_name', student.middle_name),
            'last_name': data.get('last_name', student.last_name),
            'gender': data.get('gender', student.gender),
            'birth_date': data.get('birth_date', student.birth_date),
            'gr_no': data.get('gr_no', student.gr_no),
            'category_id': data.get('category_id', student.category_id.id if student.category_id else None),
        })

        student.partner_id.write({
            'email': data.get('email', student.partner_id.email),
            'phone': data.get('phone', student.partner_id.phone),
            'image_1920': data.get('image') if data.get('image') else student.partner_id.image_1920,
        })

        return Response(json.dumps({'status': 'Student updated successfully'}), content_type='application/json')

    # DELETE - Remove a student
    @http.route('/api/students/<int:student_id>', type='http', auth='public', methods=['DELETE'], csrf=False)
    def delete_student(self, student_id):
        student = request.env['op.student'].sudo().browse(student_id)

        if not student.exists():
            return Response(json.dumps({'error': 'Student not found'}), content_type='application/json', status=404)

        student.unlink()
        return Response(json.dumps({'status': 'Student deleted successfully'}), content_type='application/json')



