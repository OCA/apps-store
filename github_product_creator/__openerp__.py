# -*- coding: utf-8 -*-
# Copyright (C) 2016-Today: Odoo Community Association (OCA)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
{
    'name': 'Github Connector - Odoo',
    'summary': 'Analyze Odoo modules information from Github repositories',
    'version': '10.0.1.0.0',
    'category': 'Connector',
    'license': 'AGPL-3',
    'author': 'Odoo Community Association (OCA), Sylvain LE GAL, GRAP',
    'depends': [
        'github_connector_odoo',
        'product',
    ],
    'data': [
        'data/product_attribute.xml',
        'views/view_odoo_module.xml',
        'views/view_product_template.xml',
        'views/view_product_product.xml',
    ],
    'installable': True,
}
