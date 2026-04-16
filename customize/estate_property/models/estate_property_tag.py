from odoo import fields, models, api


class EstatePropertyTag(models.Model):
    _name = 'estate.property.tag'
    _description = 'Property Tag'

    name = fields.Char(required=True, string="Property Tag")

    _sql_constraints = [
        ('check_unique_name', 'unique(name)','Tag name has been used.')
    ]