from odoo import models, fields, api, _

class OpParent(models.Model):
    _name="op.parent"
    _description = "Parent information"

    name = fields.Char('Name')
    phone = fields.Char('Phone')
    email = fields.Char('Email')
    relation = fields.Char('Relation with Child')
    student_id = fields.Many2one('op.student', string="Student")