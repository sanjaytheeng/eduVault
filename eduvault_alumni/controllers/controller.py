from odoo import http
from odoo.http import request

class AlumniController(http.Controller):
    @http.route('/alumni', type='http', auth='public', website=True)
    def alumni_list(self, **kw):
        alumni_records = request.env['alumni.alumni'].sudo().search([])
        return request.render('alumni.alumni_template', {'alumni': alumni_records})

    @http.route('/alumni/<int:alumni_id>', type='http', auth='public', website=True)
    def alumni_detail(self, alumni_id, **kw):
        alumni_record = request.env['alumni.alumni'].sudo().browse(alumni_id)
        return request.render('alumni.alumni_detail_template', {'alumni': alumni_record})