from odoo import fields, models, api, _


class EstatePropertyType(models.Model):
    _name = 'estate.property.type'
    _description = 'Estate Property Type'
    _order = "name"

    name = fields.Char(required=True, string="Property Type")
    active = fields.Boolean(
        string='Active',
        required=False)
    property_ids = fields.One2many(
        comodel_name='estate.property',
        inverse_name='property_type_id',
        string='Properties',
        required=False)
    sequence = fields.Integer('Sequence', default=1, help="Used to order stages. Lower is better.")
    offer_ids = fields.One2many(
        comodel_name='estate.property.offer',
        inverse_name='property_id',
        string='Offer',
        required=False)
    offer_count = fields.Integer(
        string='Offer Count',
        compute='_compute_offer_count',
        required=False)

    _sql_constraints = [
        ('check_unique_name', 'unique(name)','Duplicate type. Chose another type!')
    ]

    @api.depends('offer_ids')
    def _compute_offer_count(self):
        for record in self:
            count = 0
            for property in record.property_ids:
                count += len(property.offer_ids)
            record.offer_count = count

    def action_view_offers(self):
        # import pdb
        # pdb.set_trace()
        return {
            'name': _('Property Offers'),
            'type': 'ir.actions.act_window',
            'res_model': 'estate.property.offer',
            'view_mode': 'list,form',
            'target': 'current',
            'context':{},
            'domain': [('property_type_id', '=', self.id)],
        }