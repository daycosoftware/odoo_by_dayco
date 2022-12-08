# -*- coding: utf-8 -*-
{
    'name': 'Modulos de Kit de productos',
    'summary': """"
        V.1.0.0 - Permite replicar la funcionalidad por defecto de odoo, de crear suscripciones, tares y proyectos
                utilizando los productos configurados como kit con lista de materiales, el cual se leeran al confirmar
                una orden de venta, de cumplir con los requisitos se crearan lineas extras en la orden de venta
                con los productos configurados en la lista de materiales del producto kit.
    
    """,
    'author': 'daycohost',
    'company': 'daycohost',
    'depends': [
                'base', 'sale_subscription', 'product'
                ],
    'data': [
        'views/product_template_views.xml',
        'views/sale_views.xml',
    ],
    'installable': True,
    'active': True,
}
