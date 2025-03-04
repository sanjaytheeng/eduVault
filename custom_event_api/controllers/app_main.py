from odoo import http
from odoo.http import request

class EventController(http.Controller):

    @http.route('/api/events', type='http', auth='public', methods=['GET'])
    def get_events(self):
        """Fetches and returns all events."""
        events = request.env['event.event'].sudo().search([])
        event_data = [{
            'id': event.id,
            'name': event.name,
            'start_date': event.date_begin,
            'end_date': event.date_end,
            'location': event.address_id.name if event.address_id else 'N/A'
        } for event in events]

        return request.make_response(json.dumps({'status': 'success', 'data': event_data}),
                                     headers={'Content-Type': 'application/json'})

    @http.route('/api/events/<int:event_id>', type='http', auth='public', methods=['GET'])
    def get_event_by_id(self, event_id):
        """Fetches a specific event by ID."""
        event = request.env['event.event'].sudo().browse(event_id)
        if not event.exists():
            return request.make_response(json.dumps({'status': 'error', 'message': 'Event not found'}),
                                         headers={'Content-Type': 'application/json'}, status=404)

        event_data = {
            'id': event.id,
            'name': event.name,
            'start_date': event.date_begin,
            'end_date': event.date_end,
            'location': event.address_id.name if event.address_id else 'N/A'
        }

        return request.make_response(json.dumps({'status': 'success', 'data': event_data}),
                                     headers={'Content-Type': 'application/json'})