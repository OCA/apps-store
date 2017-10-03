# -*- coding: utf-8 -*-
# Copyright 2017 Onestein (<http://www.onestein.eu>)
# Copyright 2017 Alex Comba - Agile Business Group
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
{
    'name': 'Github Product Creator',
    'summary': 'Creates product variants for each module version',
    'version': '10.0.1.0.0',
    'category': 'Extra Tools',
    'license': 'AGPL-3',
    'author': 'Onestein, Agile Business Group,'
              'Odoo Community Association (OCA),',
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
