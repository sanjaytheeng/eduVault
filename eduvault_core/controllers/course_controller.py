import json
import logging

from odoo import http
from odoo.http import request, Response

_logger = logging.getLogger(__name__)

class SubjectController(http.Controller):

    @http.route('/api/course/subjects', type='http', auth='public', methods=['GET'], csrf=False)
    def get_course_subjects(self, **kwargs):
        course_id = kwargs.get('course_id')

        if not course_id:
            return request.make_response(json.dumps({'error': 'Missing course_id'}),
                                         headers={'Content-Type': 'application/json'})

        # Fetch the course record
        course = request.env['op.course'].sudo().search([('id', '=', int(course_id))], limit=1)

        if not course:
            return request.make_response(json.dumps({'error': 'Course not found'}),
                                         headers={'Content-Type': 'application/json'})

        # Fetch the subjects associated with the course
        subjects = course.subject_ids

        subject_data = []
        for subject in subjects:
            subject_data.append({
                'subject_id': subject.id,
                'name': subject.name,
                'code': subject.code,
            })

        response_data = {
            'course_id': course.id,
            'course_name': course.name,
            'subjects': subject_data,
        }

        return request.make_response(json.dumps(response_data), headers={'Content-Type': 'application/json'})

class CourseController(http.Controller):

    @http.route('/api/courses', type='http', auth='public', methods=['GET'], csrf=False)
    def get_courses(self, **kwargs):
        # \"\"\"
        # Fetch the list of active courses with related subjects.
        # Supports optional filtering by department.
        # \"\"\"
        try:
            domain = [('active', '=', True)]

            # Optional: Filter by department_id
            department_id = kwargs.get('department_id')
            if department_id:
                try:
                    department_id = int(department_id)
                    domain.append(('department_id', '=', department_id))
                except ValueError:
                    return Response(json.dumps({'error': 'Invalid department_id. Must be an integer.'}),
                                    content_type='application/json', status=400)

            # Fetch courses with applied filters
            courses = request.env['op.course'].sudo().search(domain)

            # Format course data with subjects
            course_data = []
            for course in courses:
                subject_data = []
                for subject in course.subject_ids:
                    subject_data.append({
                        'subject_id': subject.id,
                        'name': subject.name,
                        'code': subject.code,
                    })

                course_data.append({
                    'id': course.id,
                    'name': course.name,
                    'code': course.code,
                    'evaluation_type': course.evaluation_type,
                    'department': course.department_id.name if course.department_id else None,
                    'subjects': subject_data,  # Include subjects data here
                })

            return Response(json.dumps({'status': 'success', 'courses': course_data}),
                            content_type='application/json', status=200)

        except Exception as e:
            return Response(json.dumps({'status': 'error', 'message': str(e)}),
                            content_type='application/json', status=500)