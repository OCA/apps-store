# -*- coding: utf-8 -*-
# Copyright (C) 2017-Today: Odoo Community Association (OCA)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
{
    'name': 'Github product creator',
    'summary': 'Create a product variant (by version) for every module found '
               'in the Github repositories',
    'version': '10.0.1.0.0',
    'category': 'Connector',
    'license': 'AGPL-3',
    'author': 'Odoo Community Association (OCA)',
    'depends': [
        'github_connector_odoo',
        'product',
    ],
    'data': [
        'data/ir_cron.xml',
        'views/view_odoo_module.xml',
        'views/view_product_product.xml',
    ],
    'demo': [
        'demo/product_attribute.xml',
    ],
    'installable': True,
}
