from odoo import fields, models, api
import logging # Import modul logging
from dateutil.relativedelta import relativedelta # Import relativedelta
from odoo.exceptions import UserError,ValidationError
import odoo.tools.float_utils

_logger = logging.getLogger(__name__) # Inisialisasi logger untuk debugging


class EstateProperty(models.Model):
    _name = 'estate.property'
    _description = 'Estate Property'
    _order = "id desc"

    name = fields.Char(required=True, string='Title')
    description = fields.Text(
        string="Description",
        required=False)
    postcode = fields.Char(
        string='Postcode',
        required=False)
    date_availability = fields.Date(
        string='Date Availability',
        default=fields.Date.today() + relativedelta(months=3),
        copy=False,
        required=False)
    expected_price = fields.Float(
        string='Expected Price',
        required=True)
    selling_price = fields.Float(
        string='Selling Price',
        copy=False,
        readonly=True,
        required=False)
    bedrooms = fields.Integer(
        string='Bedrooms',
        default=2   ,
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
        onchange='_onchange_garden',
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
    active = fields.Boolean(default=False)
    state = fields.Selection(
        string='State',
        selection=[('new', 'New'),
                   ('offer_received', 'Offer Received'),
                   ('offer_accepted', 'Offer Accepted'),
                   ('sold', 'Sold'),
                   ('canceled', 'Canceled'),],
        required=True, copy=False, default='new')
    partner_id = fields.Many2one("res.partner", copy=False, string="Buyer")
    users_id = fields.Many2one("res.users", string="Salesman", default=lambda self: self.env.user)
    property_type_id = fields.Many2one(
        comodel_name='estate.property.type',
        string='Property Type',
        required=True)
    tag_ids = fields.Many2many(
        comodel_name='estate.property.tag',
        string='Tags')
    offer_ids = fields.One2many(
        comodel_name='estate.property.offer',
        inverse_name='property_id',
        string='Offer',
        required=False)
    total_area = fields.Integer(
        string='Total Area',
        compute='_compute_total_area',
        required=False)
    best_price = fields.Float(
        string='Best Price',
        compute='_compute_best_price',
        required=False)
    active = fields.Boolean(
        string='Active',
        default=True,
        required=False)


    _sql_constraints = [
        ('check_expected_price_is_positive', 'CHECK(expected_price > 0.0)', 'The expected price must be a positive number!'),
        ('check_selling_is_positive', 'CHECK(selling_price > 0.0)', 'The selling price must be a positive number!')
    ]

    @api.constrains('selling_price')
    def _check_selling_price_constraint(self):
        for record in self:
            percentage = abs(record.selling_price / record.expected_price) * 100
            if percentage <= 80:
                raise ValidationError("The selling price cannot be under 90% of the expected price!")

    @api.depends('living_area','garden_area')
    def _compute_total_area(self):
        for property in self:
            property.total_area = property.living_area + property.garden_area

    @api.depends('offer_ids.price')
    def _compute_best_price(self):
        for property_record in self:
            prices = property_record.offer_ids.mapped('price')
            if prices:
                property_record.best_price = max(prices)
            else:
                property_record.best_price = 0.0

    @api.onchange('garden')
    def _onchange_garden(self):
        for property in self:
            if property.garden:
                property.garden_orientation = 'north'
                property.garden_area = 50

    def act_btn_sold(self):
        for record in self:
            if record.state == 'canceled':
                raise UserError('Property has been cancelled')
            else:
                record.state = 'sold'

    def act_btn_cancel(self):
        for record in self:
            if record.state == 'sold':
                raise UserError('Property has been sold')
            else:
                record.state = 'canceled'

    @api.model
    def create(self, vals):
        record = super().create(vals)
        if record.offer_ids:
            record.state = 'offer_received'
        else:
            record.state = 'new'
        return record

    def write(self, vals):
        res = super().write(vals)
        for record in self:
            if record.offer_ids and record.state == 'new':
                record.state = 'offer_received'
            elif not record.offer_ids and record.state == 'offer_received':
                record.state = 'new'
        return res

    @api.ondelete(at_uninstall=False)
    def _unlink_if_property_new_or_canceled(self):
        for record in self:
            if record.state not in ['new','canceled']:
                raise UserError('Property not new or cancelled.')

    def action_print_qweb_report(self):
        # return True
        return self.env.ref('estate_property.report_estate_property_details').report_action(self)