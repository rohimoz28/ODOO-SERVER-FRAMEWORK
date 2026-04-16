from odoo import fields, models, api
from datetime import date, timedelta
from odoo.exceptions import UserError

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
    validity = fields.Integer(
        string='Validity',
        default=7,
        required=False)
    date_deadline = fields.Date(
        string='Date Deadline',
        inverse='_inverse_date_deadline',
        compute='_compute_date_deadline',
        required=False)

    @api.depends('validity')
    def _compute_date_deadline(self):
        for property in self:
            if property.validity:
                property.date_deadline = date.today() + timedelta(days=property.validity)

    def _inverse_date_deadline(self):
        for property in self:
            if property.date_deadline:
                property.validity = (property.date_deadline - date.today()).days

    def act_offer_accepted(self):
        for record in self:
            record.property_id.partner_id = record.partner_id
            record.property_id.selling_price = record.price
            record.status = 'accepted'
            record.property_id.state = 'offer_accepted'


    def act_offer_refused(self):
        for record in self:
            pass