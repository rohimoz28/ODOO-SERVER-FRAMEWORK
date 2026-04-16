from odoo import fields, models, api


class EstatePropertyType(models.Model):
    _name = 'estate.property.type'
    _description = 'Estate Property Type'

    name = fields.Char(required=True, string="Property Type")

    _sql_constraints = [
        ('check_unique_name', 'unique(name)','Duplicate type. Chose another type!')
    ]