from odoo import http
from odoo.http import request
import pytz
import json


class TimetableController(http.Controller):

    @http.route('/api/timetable', type='http', auth='public', methods=['GET'], csrf=False)
    def get_timetable(self, **kwargs):
        """
        Fetch timetable data based on the view `view_op_session_tree`.
        """
        try:
            # Fetch session data with required fields
            sessions = request.env['op.session'].sudo().search([
                ('state', '=', 'confirm'),
                ('active', '=', True)
            ])

            if not sessions:
                return request.make_response(
                    json.dumps({'status': 'success', 'message': 'No sessions found'}),
                    [('Content-Type', 'application/json')]
                )

            # Prepare the data in a format suitable for Flutter
            timetable_data = []

            # Get the user's timezone to adjust the times accordingly
            user_timezone = request.env.user.tz or 'UTC'
            tz = pytz.timezone(user_timezone)

            for session in sessions:
                session_start = session.start_datetime.astimezone(tz)
                session_end = session.end_datetime.astimezone(tz)

                # Prepare session data with the required fields
                timetable_data.append({
                    'faculty_id': session.faculty_id.name,
                    'batch_id': session.batch_id.name,
                    'subject_id': session.subject_id.name,
                    'classroom_id': session.classroom_id.name if session.classroom_id else 'N/A',
                    'start_datetime': session_start.strftime('%Y-%m-%d %H:%M:%S'),
                    'end_datetime': session_end.strftime('%Y-%m-%d %H:%M:%S'),
                    'state': session.state,
                    # Hide course_id and type based on your view definition
                    'course_id': session.course_id.name,  # Hidden in the view
                    'type': session.type,  # Hidden in the view
                })

            # Return JSON data
            return request.make_response(
                json.dumps({'status': 'success', 'data': timetable_data}),
                [('Content-Type', 'application/json')]
            )

        except Exception as e:
            # Catch any error and return a failure response
            return request.make_response(
                json.dumps({'error': str(e)}),
                [('Content-Type', 'application/json')]
            )