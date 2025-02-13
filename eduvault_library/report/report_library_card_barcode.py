

import time
from odoo import models, api


class ReportLibraryCardBarcode(models.AbstractModel):
    _name = "report.eduvault_library.report_library_card_barcode"
    _description = "Library Card Barcode Report"

    @api.model
    def _get_report_values(self, docids, data=None):
        docs = self.env['op.library.card'].browse(docids)
        docargs = {
            'doc_model': 'op.library.card',
            'docs': docs,
            'time': time,
        }
        return docargs
