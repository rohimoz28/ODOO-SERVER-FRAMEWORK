from odoo import fields, models, api


class EstatePropertyOffer(models.Model):
    _name = 'estate.property.offer'
    _description = 'Property Offer'

    name = fields.Char(required=True)
    price = fields.Float(
        string='Price',
        required=False)
    status = fields.Selection(
        string='Status',
        selection=[('accepted', 'Accepted'), ('refused', 'Refused')],
        required=False, copy=False)
    partner_id = fields.Many2one(
        comodel_name='res.partner',
        string='Buyer',
        required=True)
    property_id = fields.Many2one(
        "estate.property",
        string="Property",
        required=True,
    )
