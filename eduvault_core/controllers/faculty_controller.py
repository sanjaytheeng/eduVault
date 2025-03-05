import json
import logging
from odoo import http
from odoo.http import request, Response

_logger = logging.getLogger(__name__)


class FacultyController(http.Controller):

    @http.route('/api/faculty', type='http', auth='public', methods=['GET'], csrf=False)
    def get_faculties(self, **kwargs):
        """
        Fetch a list of active faculties.
        Supports optional filtering by department.
        """
        try:
            domain = [('active', '=', True)]

            # Optional: Filter by department_id
            department_id = kwargs.get('department_id')
            if department_id:
                try:
                    department_id = int(department_id)
                    domain.append(('main_department_id', '=', department_id))
                except ValueError:
                    return Response(json.dumps({'error': 'Invalid department_id. Must be an integer.'}),
                                    content_type='application/json', status=400)

            # Fetch faculty records
            faculties = request.env['op.faculty'].sudo().search(domain)

            faculty_data = [{
                'id': faculty.id,
                'name': f"{faculty.first_name} {faculty.middle_name or ''} {faculty.last_name}".strip(),
                'gender': faculty.gender,
                'birth_date': faculty.birth_date.strftime('%Y-%m-%d') if faculty.birth_date else None,
                'email': faculty.partner_id.email,
                'phone': faculty.partner_id.phone,
                'department': faculty.main_department_id.name if faculty.main_department_id else None,
                'subjects': [subject.name for subject in faculty.faculty_subject_ids]
            } for faculty in faculties]

            return Response(json.dumps({'status': 'success', 'faculties': faculty_data}),
                            content_type='application/json', status=200)

        except Exception as e:
            return Response(json.dumps({'status': 'error', 'message': str(e)}),
                            content_type='application/json', status=500)

    @http.route('/api/faculty/<int:faculty_id>', type='http', auth='public', methods=['GET'], csrf=False)
    def get_faculty_details(self, faculty_id, **kwargs):
        """
        Fetch details of a specific faculty member by ID.
        """
        try:
            faculty = request.env['op.faculty'].sudo().browse(faculty_id)

            if not faculty.exists():
                return Response(json.dumps({'error': 'Faculty not found'}), content_type='application/json', status=404)

            faculty_data = {
                'id': faculty.id,
                'name': f"{faculty.first_name} {faculty.middle_name or ''} {faculty.last_name}".strip(),
                'gender': faculty.gender,
                'birth_date': faculty.birth_date.strftime('%Y-%m-%d') if faculty.birth_date else None,
                'email': faculty.partner_id.email,
                'phone': faculty.partner_id.phone,
                'department': faculty.main_department_id.name if faculty.main_department_id else None,
                'subjects': [subject.name for subject in faculty.faculty_subject_ids]
            }

            return Response(json.dumps({'status': 'success', 'faculty': faculty_data}),
                            content_type='application/json', status=200)

        except Exception as e:
            return Response(json.dumps({'status': 'error', 'message': str(e)}),
                            content_type='application/json', status=500)

    class FacultyTimetableController(http.Controller):

        @http.route('/api/faculty/<int:faculty_id>/timetable', type='http', auth='public', methods=['GET'],
                    csrf=False)
        def get_faculty_timetable(self, faculty_id, **kwargs):
            """
            Fetch the timetable for a specific faculty member by ID.
            """
            try:
                faculty = request.env['op.faculty'].sudo().browse(faculty_id)

                if not faculty.exists():
                    return Response(json.dumps({'error': 'Faculty not found'}), content_type='application/json',
                                    status=404)

                # Fetch the sessions associated with the faculty
                sessions = request.env['op.session'].sudo().search([('faculty_id', '=', faculty_id)])

                timetable_data = [{
                    'session_id': session.id,
                    'course': session.course_id.name,
                    'subject': session.subject_id.name,
                    'start_time': session.start_datetime.strftime('%Y-%m-%d %H:%M:%S'),
                    'end_time': session.end_datetime.strftime('%Y-%m-%d %H:%M:%S'),
                    'classroom_id': {
                        'id': session.classroom_id.id,
                        'name': session.classroom_id.name
                    }
                } for session in sessions]

                response_data = {
                    'status': 'success',
                    'faculty_name': f"{faculty.first_name} {faculty.middle_name or ''} {faculty.last_name}".strip(),
                    'timetable': timetable_data
                }

                return Response(json.dumps(response_data), content_type='application/json', status=200)

            except Exception as e:
                _logger.error("Error fetching timetable: %s", str(e))
                return Response(json.dumps({'status': 'error', 'message': str(e)}), content_type='application/json',
                                status=500)
