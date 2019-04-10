from odoo import _, api, fields, models


class StockRule(models.Model):
    _inherit = 'stock.rule'

    def _prepare_purchase_order(self, product_id, product_qty, product_uom, origin,
                                values, partner):
        res = super(StockRule, self). _prepare_purchase_order(product_id, product_qty, product_uom, origin,
                                values, partner)
        if origin and 'SO' in origin:
            operating_unit_id = self.env['sale.order'].search(
                [('name', '=', origin)]).warehouse_id.operating_unit_id.id

            res.update({'operating_unit_id': operating_unit_id,
                        'requesting_operating_unit_id': operating_unit_id})

            type_obj = self.env['stock.picking.type']
            types = type_obj.search([('code', '=', 'incoming'),
                                     ('warehouse_id.operating_unit_id', '=',
                                      operating_unit_id)])
            if types:
                types = types[:1].id
                res.update({'picking_type_id': types})

        return res
