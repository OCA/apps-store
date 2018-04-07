# -*- coding: utf-8 -*-
# Copyright (C) 2017-Today: Odoo Community Association (OCA)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
{
    'name': 'Website Apps Store',
    'summary': 'Website AppStore',
    'version': '10.0.1.0.0',
    'website': 'http://www.bizzappdev.com',
    'category': 'Connector',
    'license': 'AGPL-3',
    'author': 'Bizzappdev',
    'depends': [
        'website_sale',
        'apps_download',
        'apps_product_creator',
    ],
    'data': [
        'views/assets.xml',
        'views/templates.xml',
    ],
    'demo': [
    ],
    'installable': True,
    'auto_install': False,
    'application': False
}
