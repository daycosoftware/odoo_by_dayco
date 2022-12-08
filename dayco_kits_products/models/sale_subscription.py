# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
from odoo import fields, models

class SaleOrderLineInherit(models.Model):
    _inherit = 'sale.order.line'

    order_line_id_product_of_kit = fields.Many2one('sale.order.line', help="Id de la linea de la orden que genera productos con kits")

class SaleOrderInherit(models.Model):
    _inherit = 'sale.order'

    def _action_confirm(self):
        """ Esta herencia permite agregar el método nuevo llamado 'create_order_lines_extras'"""
        self.create_order_lines_extras()
        res = super(SaleOrderInherit, self)._action_confirm()
        return res

    def create_order_lines_extras(self):
        """ Este metodo nuevo, permite verificar los productos seleccionados en la venta, para saber cuales cuentan con lista de materiales
            como kit, con el fin de agregar los productos configurados como líneas  en la orden se venta.
            Adicionalmente lee las listas de materiales y filtra por la variante del producto, y toma siempre la primera según  la secuencia.

            Nota: Los productos calificados son los que contengan el campo 'is_product_kits' activo en la ficha del producto, y que a su vez
            contenga lista de materiales.
         """
        order_line_origin = self.order_line
        new_data_order_line = []
        for line in order_line_origin:
            if line.product_id.is_product_kits and line.product_id.bom_ids:
                bom_ids = line.product_id.bom_ids.filtered(lambda bom: bom.product_tmpl_id == line.product_template_id and bom.product_id == line.product_id)
                if not bom_ids:
                    bom_ids = line.product_id.bom_ids.filtered(lambda bom: bom.product_tmpl_id == line.product_template_id and not bom.product_id)
                if bom_ids:
                    bom_ids.sorted(key=lambda k: (k['sequence']))
                    if bom_ids[0]:
                        # for bom in bom_ids:
                        bom_id = bom_ids[0]
                        if bom_id.bom_line_ids:
                            for bom_line in bom_id.bom_line_ids:
                                new_line = {}
                                if bom_line:
                                    new_line.update({
                                            'order_id': self.id,
                                            'price_unit': 0.0,
                                            'name': bom_line.product_id.name,
                                            'product_id': bom_line.product_id.id,
                                            'product_uom_qty': bom_line.product_qty * line.product_uom_qty,
                                            'product_uom': bom_line.product_uom_id.id,
                                            'company_id': self.env.company.id,
                                            'order_line_id_product_of_kit': line.id,
                                        })
                                    new_data_order_line.append(new_line)
        if new_data_order_line:
            self.env['sale.order.line'].create(new_data_order_line)

    def create_subscriptions(self):
        """ Esta herencia de este metodo, permite agregarle la actualizacion del precio de las suscripciones creadas mediante
            el proceso de productos con lista de materiales como kit (Con productos como servicios).
        """
        res = super(SaleOrderInherit, self).create_subscriptions()

        if res:
            subscriptions_ids = self.env['sale.subscription'].browse(res)
            if subscriptions_ids:
                order_lines_product_kits = self.order_line.filtered(lambda line: line.order_line_id_product_of_kit and line.subscription_id)
                if order_lines_product_kits:
                    for subscription_id in order_lines_product_kits.subscription_id:
                        for subscription_line in subscription_id.recurring_invoice_line_ids:  # Productos de la suscripcion
                            subscription_line.onchange_product_quantity()
        return res