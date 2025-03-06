from odoo import http
from odoo.http import request
import json


class ExamSessionController(http.Controller):

    @http.route('/api/exam_session/data', type='http', auth='public', methods=['GET'], csrf=False)
    def get_exam_sessions(self):
        sessions = request.env['op.exam.session'].sudo().search([])
        session_data = []

        for session in sessions:
            exams = request.env['op.exam'].sudo().search([('session_id', '=', session.id)])
            subjects = {}

            for exam in exams:
                subject_name = exam.subject_id.name if exam.subject_id else 'Unknown'
                attendees = request.env['op.exam.attendees'].sudo().search([('exam_id', '=', exam.id)])

                # Fetching attendee names and their marks
                for attendee in attendees:
                    student_name = attendee.student_id.name
                    marks = attendee.marks if attendee.marks else 'Not Assigned'

                    if subject_name not in subjects:
                        subjects[subject_name] = []

                    subjects[subject_name].append({
                        'student_name': student_name,
                        'marks': marks
                    })

            session_data.append({
                'exam_session': session.name,
                'exam_code': session.exam_code,
                'course': session.course_id.name,
                'batch': session.batch_id.name,
                'start_date': session.start_date.strftime('%Y-%m-%d') if session.start_date else 'Not Assigned',
                'end_date': session.end_date.strftime('%Y-%m-%d') if session.end_date else 'Not Assigned',
                'exam_type': session.exam_type.name,
                'evaluation_type': session.evaluation_type,
                'venue': session.venue.name if session.venue else 'Not Assigned',
                'state': session.state,
                'subjects': subjects
            })

        # Return the response as a JSON string
        return http.Response(
            json.dumps({'exam_sessions': session_data}),
            content_type='application/json'
        )