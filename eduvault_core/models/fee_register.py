from odoo import fields, api, models, _

class OpFeeRegister(models.Model):
    _name="op.fee.register"
    _description="This is a fee register model"

    name = fields.Many2one('op.student', string="Name")
    date = fields.Date(string="Date")
    batches = fields.Many2one('op.batch', string="Batch")
    courses = fields.Many2one('op.course', string="Course")
    fee_structures = fields.Char('Fee Structure')
    journal = fields.Char('journal')