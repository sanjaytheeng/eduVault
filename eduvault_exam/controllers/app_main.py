import logging
from odoo import http
from odoo.http import request, Response
import json

_logger = logging.getLogger(__name__)


class ExamSessionController(http.Controller):

    @http.route('/api/exam/subjects', type='http', auth='public', methods=['GET'], csrf=False)
    def get_exam_sessions(self, **kwargs):
        try:
            # Fetch all exam sessions
            exam_sessions = request.env['op.exam.session'].sudo().search([])

            # Group sessions by course
            grouped_sessions = {}
            for session in exam_sessions:
                course_id = session.course_id.id if session.course_id else None
                course_name = session.course_id.name if session.course_id else None
                if course_id not in grouped_sessions:
                    grouped_sessions[course_id] = {
                        'course_name': course_name,
                        'sessions': []
                    }
                grouped_sessions[course_id]['sessions'].append({
                    'id': session.id,
                    'name': session.name,
                    'start_date': session.start_date.strftime('%Y-%m-%d %H:%M:%S') if session.start_date else None,
                    'end_date': session.end_date.strftime('%Y-%m-%d %H:%M:%S') if session.end_date else None,
                })

            return Response(json.dumps({'status': 'success', 'data': grouped_sessions}),
                            content_type='application/json', status=200)

        except Exception as e:
            _logger.error("Error fetching exam sessions: %s", str(e))
            return Response(json.dumps({'status': 'error', 'message': str(e)}),
                            content_type='application/json', status=500)


class ExamController(http.Controller):

    @http.route('/api/exam/subjects/<int:course_id>', type='http', auth='public', methods=['GET'], csrf=False)
    def get_course_subjects(self, course_id, **kwargs):
        try:
            # Fetch the course
            course = request.env['op.course'].sudo().browse(course_id)

            if not course.exists():
                return Response(json.dumps({'error': 'Course not found'}), content_type='application/json', status=404)

            # Fetch the subjects related to the course
            subjects = course.subject_ids

            # Format subject data
            subject_data = [{
                'id': subject.id,
                'name': subject.name,
                'code': subject.code,
            } for subject in subjects]

            return Response(json.dumps({'status': 'success', 'data': subject_data}),
                            content_type='application/json', status=200)

        except Exception as e:
            _logger.error("Error fetching subjects: %s", str(e))
            return Response(json.dumps({'status': 'error', 'message': str(e)}),
                            content_type='application/json', status=500)
