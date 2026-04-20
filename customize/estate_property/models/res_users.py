from odoo import fields, models, api


class InheritResUsers (models.Model):
    _inherit = 'res.users'

    property_ids = fields.One2many(
        comodel_name='estate.property',
        inverse_name='users_id',
        string='Real Estate Properties',
        required=False)
