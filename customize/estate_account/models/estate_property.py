from odoo import fields, models, api
from odoo.exceptions import UserError,ValidationError


class InheritEstateProperty(models.Model):
    _inherit = 'estate.property'

    def act_btn_sold(self):
        for record in self:
            accepted_offer = record.offer_ids.filtered(lambda o: o.status == 'accepted')

            if not accepted_offer:
                raise UserError("Cannot set a property as sold without an accepted offer.")

            selling_price = accepted_offer.price
            # Menghitung komisi 6%
            commission = selling_price * 0.06
            # Menghitung biaya administrasi
            administrative_fees = 100.00

            self.env["account.move"].create({
                "partner_id": accepted_offer.partner_id.id,
                "move_type": 'out_invoice',
                "invoice_line_ids": [
                    (0, 0, {
                        'name': "6% Commission",
                        'quantity': 1,
                        'price_unit': commission,
                    }),
                    (0, 0, {
                        'name': "Administrative Fees",
                        'quantity': 1,
                        'price_unit': administrative_fees,
                    }),
                ],
            })

        return super().act_btn_sold()