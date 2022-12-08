# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models
from odoo.osv import expression


class ProductTemplateInherit(models.Model):
    _inherit = 'product.template'

    is_product_kits = fields.Boolean('Producto Kits', default=False)