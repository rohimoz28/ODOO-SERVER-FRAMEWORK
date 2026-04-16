from odoo import fields, models


class EstateProperty(models.Model):
    _name = 'estate.property'
    _description = 'Estate Property'

    name = fields.Char(required=True)
    description = fields.Text(
        string="Description",
        required=False)
    postcode = fields.Char(
        string='Postcode',
        required=False)
    date_availability = fields.Date(
        string='Date Availability',
        required=False)
    expected_price = fields.Float(
        string='Expected Price',
        required=True)
    selling_price = fields.Float(
        string='Selling Price',
        required=False)
    bedrooms = fields.Integer(
        string='Bedrooms',
        required=False)
    living_area = fields.Integer(
        string='Living Area',
        required=False)
    facades = fields.Integer(
        string='Facades',
        required=False)
    garage = fields.Boolean(
        string='Garage',
        required=False)
    garden = fields.Boolean(
        string='Garden',
        required=False)
    garden_area = fields.Integer(
        string='Garden Area',
        required=False)
    garden_orientation = fields.Selection(
        string='Garden Orientation',
        selection=[('north', 'North'),
                   ('south', 'South'),
                   ('east', 'East'),
                   ('west', 'West')],
        required=False, )
